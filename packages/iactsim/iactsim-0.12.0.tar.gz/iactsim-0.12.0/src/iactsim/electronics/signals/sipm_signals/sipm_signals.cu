// Copyright (C) 2024- Davide Mollica <davide.mollica@inaf.it>
// SPDX-License-Identifier: GPL-3.0-or-later
//
// This file is part of iactsim.
//
// iactsim is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// iactsim is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with iactsim.  If not, see <https://www.gnu.org/licenses/>.

//////////////////////////////////////////////////////////////////
//////////////////////////// Content /////////////////////////////
//                                                              //
////// Device functions                                         //
//                                                              //
// __device__ borel_pmf                                         //
// __device__ borel_generator                                   //
// __device__ waveform_normalization                            //
// __device__ poisson_interarrival_time                         //
//                                                              //
////// Kernels                                                  //
//                                                              //
// __global__ sipm_signals                                      //
//                                                              //
//////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////

#include <curand_kernel.h>

extern "C"{

__device__ float interp1d_text(float x, float inv_dx, float start_x, cudaTextureObject_t& tex) {
    float u = (x-start_x)*inv_dx;
    return tex1D<float>(tex, u+0.5f);
}

/**
 * @brief Calculates the Borel probability mass function (PMF).
 *
 * This function computes the probability mass function of the Borel
 * distribution at a given value of ``k`` and with parameter ``l`` (lambda).
 * The Borel distribution is a discrete probability distribution arising
 * in the context of branching processes and queueing theory.
 *
 * @param k The non-negative integer value at which to evaluate the PMF.  Must be >= 0.
 * @param l The parameter of the Borel distribution (lambda). Must be in the range (0, 1).
 *
 * @return The probability mass function value at ``k``, given parameter ``l``. Returns a float.
 *          Returns 0 if k < 0.  Returns 0 if l <=0 or l >= 1.
 *
 * @details
 * The Borel distribution's PMF is given by:
 *   P(K = k) = (exp(-lambda * k) * (lambda * k)^(k-1)) / k!   for k = 1, 2, 3,...
 *          and 0 for k = 0.
 *
 * This implementation uses the following formula for numerical stability,
 * avoiding potential overflow or underflow with large factorials:
 *
 *   log(P(K=k)) = (k-1) * log(l*k) - l*k - lgamma(k+1)
 *   P(K=k) = exp(log(P(K=k)))
 *
 * where ``lgamma(k+1)`` is the natural logarithm of the gamma function of (k+1), which is equal to log(k!).
 *
 * @warning The input ``l`` must be within the range (0, 1). Values outside this range
 *          will return 0.  Input ``k`` should be a non-negative integer.
 *
 */
__device__ float borel_pmf(float k, float l)
{
    float logbr = fmaf(k-1.f, __logf(fmaf(l, k, 0.f)), -fmaf(l, k, lgammaf(k+1.f)));
    return __expf(logbr);
}

/**
 * @brief Generates a random variate from the Borel distribution using inversion sampling.
 *
 * This function implements the inversion sampling method to generate a random
 * number from the Borel distribution with parameter ``l`` (lambda).
 *
 * @param l The parameter of the Borel distribution (lambda).  Must be in the range (0, 1).
 * @param s A reference to a ``curandStatePhilox4_32_10_t`` object, representing the
 *          state of the Philox4x32-10 pseudo-random number generator. This state
 *          must be initialized before calling this function.
 *
 * @return A random float from the Borel distribution with parameter ``l``.
 *          Returns 1.0f if ``l`` is very small (< 1e-4f).
 *
 */
__device__ float borel_generator(float l, curandStatePhilox4_32_10_t &s)
{
    if (l<1e-4f) return 1.f;
    
    float u = curand_uniform(&s);

    float p1 = 0.f;
    float k = 0.f;
    while (true) {
        float p2 = p1 + borel_pmf(k+1.f, l);
        if ( ((u > p1) & (u <= p2)) | (p2-p1<1e-9f) ) {
            return k + 1.f;
        }
        p1 = p2;
        k += 1.f;
    }
}

/**
 * @brief Calculates a normalization factor for a waveform, accounting for prompt cross-talk and micro-cells gain dispersion.
 *
 * This function simulates the effects of cross-talk and variations in micro-cell gain
 * on the overall normalization of a waveform.
 *
 * @param state A reference to a ``curandStatePhilox4_32_10_t`` object, representing the
 *              state of the Philox4x32-10 pseudo-random number generator.  This state
 *              must be initialized before calling this function.
 * @param n_discharges  The number of events to simulate (main discharge + xt discharges).  This effectively controls
 *              how many random samples are summed to produce the normalization factor.
 * @param std_ucells The standard deviation of the micro-cell gain.  This parameter
 *                   scales the contribution of each random sample.
 *
 * @return The calculated normalization factor (a float).
 *
 * @details
 * The normalization factor is computed as the sum of ``n_discharges`` independent random
 * variables, each drawn from a normal distribution with mean 1.0 and standard
 * deviation ``std_ucells``.
 *
 */
__device__ float waveform_normalization(curandStatePhilox4_32_10_t &state, float n_discharges, float std_ucells)
{
    float normalization_factor = 0.0f;
    for (int k=0; k<(int)n_discharges; k++) normalization_factor += fmaf(curand_normal(&state), std_ucells, 1.0f);
    return normalization_factor;
}

/**
 * @brief Generates a Poisson inter-arrival time.
 *
 * This function calculates a random inter-arrival time from an exponential
 * distribution, which is equivalent to the inter-arrival times in a Poisson process.
 *
 * @param state A reference to a ``curandStatePhilox4_32_10_t`` object, representing the
 *              state of the Philox4x32-10 pseudo-random number generator. This state
 *              must be initialized before calling this function.
 * @param inv_bkg_rate The inverse of the background rate of the Poisson process.
 *                     This represents the mean inter-arrival time.
 *
 * @return A random float representing the inter-arrival time.
 * 
 */
__device__ float poisson_interarrival_time(curandStatePhilox4_32_10_t &state, float inv_bkg_rate)
{
    return -fmaf(__logf(curand_uniform(&state)),  inv_bkg_rate, 0.f);
}

__device__ __forceinline__ int get_lane_id() {
    // threadIdx.x % 32
    return threadIdx.x & 0x1f; 
}

/**
 * @brief Block-level parallel prefix sum (cumulative sym).
 * 
 * This function converts all the generated interarrival times 
 * into an absolute timing:
 *      
 * E.g:
 *     
 *     - [dt0, dt1, dt2] -> [dt0, dt0+dt1, dt0+dt1+dt2]
 * 
 * @param pe_dt A thread generated inter-arrival time.
 * @param shared_temp A temporary array where to compute all warps cumulative sum.
 * 
 */
__device__ float block_prefix_sum(float pe_dt, float* shared_temp) {
    int tid = threadIdx.x;
    
    // Cumulative sum of the whole warp
    // At each step get 'pe_dt' from the warp 'lane - offset'
    // and sum its own 'pe_dt' only if the offset is valid
    for (int offset = 1; offset < 32; offset *= 2) {
        float up = __shfl_up_sync(0xFFFFFFFF, pe_dt, offset);
        if (get_lane_id() >= offset) 
            pe_dt += up;
    }
    
    // Write the sum (the last element of the cumulative) to shared memory
    if (get_lane_id() == 31) 
        shared_temp[threadIdx.x >> 5] = pe_dt;
    
    // Wait until all warps have finished
    // Now shared_temp[warp0,warp1,...,warpN] is filled 
    // with the maximum temporal extention of each warp
    __syncthreads();
    
    // Just the first warp
    if (threadIdx.x < 32) {
        // Here threadIdx.x is equivalent to the lane
        int lane = threadIdx.x;
        // so this skips non-existing wraps
        int n_warps = blockDim.x >> 5;
        // Get from shared memory
        float warp_sum = (lane < n_warps) ? shared_temp[lane] : 0.0f;

        // Cumulative sum of warps
        for (int offset = 1; offset < 32; offset *= 2) {
            float up = __shfl_up_sync(0xFFFFFFFF, warp_sum, offset);
            if (lane >= offset)
                warp_sum += up;
        }

        // Write to shared memory
        if (lane < n_warps)
            shared_temp[lane] = warp_sum;
    }
    // Now shared_temp[warp0,warp1,...,warpN] is filled
    // with the actual last time of each warp (e.g. [0.007, 0.04, ..., 1.2])
    __syncthreads();
    
    // Each thread has a relative (to the warp) time offset pe_dt
    // Now add the cumulative sum of warps to have the absolute timing
    // (i.e. add the last cumulative time of the previous warp, in shared memory)
    if (threadIdx.x >= 32)
        pe_dt += shared_temp[threadIdx.x / 32 - 1];
    
    // This is the poissonian-event time in the specified time window
    return pe_dt;
}

/**
 * @brief Computes the formed SiPM signals.
 *
 * This kernel function simulates the response of Silicon Photo-Multipliers (SiPMs)
 * by superimposing single photo-electron (PE) waveforms based on PE arrival time,
 * SiPM cross-talk, SiPM microcells gain dispersion and SiPM PE-background noise.  
 * It operates on a per-pixel and per-channel basis, assigning a CUDA block per pixel per channel.
 *
 * @param windows Array of time windows for each channel.  Defines the time ranges
 *                over which signals are computed. ``windows[windows_map[channel] : windows_map[channel+1]]``
 *                is the time window for ``channel``.
 * @param windows_map Array indicating the starting  and ending index of the time window for each channel
 *                      within the ``windows`` array.
 * @param signals Output array where the computed SiPM signals are stored.  The signal for
 *                a given channel and pixel is stored in a contiguous block.
 *                ``signals[start_signals[channel] + pixel_id * n_window : start_signals[channel] + (pixel_id + 1) * n_window]``
 *                where n_window = windows_map[channel+1] - windows_map[channel].
 *                The array does not need to be initialized before the kernel invocation.
 * @param signals_map Array indicating the starting index and ending index of each channel inside the array signals.
 * @param n_channels Number of channels.
 * @param t0s Array of discharge times for each pixel.
 * @param map Array that maps pixel indices to the range of their corresponding
 *            discharge times in the ``t0s`` array.  Specifically, ``t0s[map[pixel_id]:map[pixel_id+1]]``
 *            provides the discharge times for ``pixel_id``.
 * @param waveforms Array containing the texture pointer of all channel waveforms.
 * @param inv_dt_waveforms Array containing the inverse of the time spacing (dt) for each
 *                         waveform.
 * @param t_start_waveforms Array indicating the starting time of each waveform.
 * @param gains Array containing the pulse peak amplitued for each pixel for each channel (n_pixels*n_channels size)
 * @param xt Array of cross-talk probabilities for each pixel.  This represents the probability
 *           that a discharge in one microcell will trigger a discharge in an adjacent microcell.
 * @param std_ucells Array of microcell gain dispersions for each pixel. This models the
 *                   variation in the charge produced by different microcells for a single photon.
 * @param mask Array indicating whether a pixel is masked (1) or active (0). Masked pixels
 *             will have zero signal.
 * @param inv_bkg_rate Array of inverse background rates for each pixel (in units of time).  This is
 *                     used to generate background noise events.
 * @param bkg_start Start time for background noise generation.
 * @param bkg_end End time for background noise generation.
 * @param seed Array of random number generator seeds, one for each pixel.
 * @param n_pixels Number of pixels.
 *
 * 
 * @warning
 * 1. The number of blocks must be at least ``n_pixels*n_channels`` (i.e. a block per pixel per channel)
 * 2. The size of the shared memory buffer must be equal to ``(max_window_size+n_threads*2 + 32) * sizeof(float)``.
 *
 * @details
 * The kernel is launched with a 1D grid of blocks, where each block is responsible for
 * computing the signal for a single (pixel, channel) combination.  Each block uses
 * shared memory (``shared_buffer``) to store the intermediate signal, improving performance
 * by reducing global memory accesses.
 * 
 * The signal computation involves the following steps:
 * 
 * 1. Determine the block assigned channel and pixel. Initialize the shared memory buffer to zero.
 * 
 * 2. Input signal
 * 
 *      2a. Initialize a ``curandStatePhilox4_32_10_t`` random number generator for the pixel using the provided seed.
 *          Each pixel has a unique seed per event. This allows the signals of each channel to be computed in different stages.
 * 
 *      2b. Iterate through the photon arrival times associated with the current pixel. For each photon:
 *   
 *          - calculate the number of cross-talk photons using a Borel distribution;
 *          - calculate the microcell gain variation, incorporating gain dispersion using a normal distribution;
 *          - superimpose the single-photon waveform onto the shared memory buffer, interpolating the channel waveform.
 * 
 * 3. Background signal
 * 
 *      3a. Re-initialize the ``curandStatePhilox4_32_10_t`` random number generator with a seed per thread.
 *
 *      3b. Heach thread generates a background noise event extracting
 *          - a number of cross-talk photons;
 *          - a micro-cell gain;
 *          - a poissoninan inter-arrival time;
 *
 *      3c. The actual time is computed with a parallel cumulative sum of all extracted times.
 *          All generated events are stored in shared memory.
 * 
 *      3d. Generated events are processed one-by-one. The signal accross the time-window 
 *          is updated in parallel in the shared memory buffer.
 * 
 * 4. Copy the computed signal from the shared memory buffer to the global ``signals`` array.
 * 
 */
__global__ void sipm_signals(
    // Time windows
    const float* windows, // windows where to compute the signals for each channel
    const int* windows_map, // where the window of each channel starts and ends in the ``windows`` array
    // Channels signals
    float* signals, // computed signals
    const int* signals_map, // where the signals of each channel starts and ends in ``signals``
    bool* skip_channel,
    int n_channels, // number of channels
    // Arrival times
    const float* t0s, // discharge times
    const int* map, // discharge times of pixel n: t0s[map[n]:map[n+1]]
    // Waveforms
    const unsigned long long* textures, // one for each channel
    const float* inv_dt_waveforms, // invers of the x-spacing of each waveform
    const float* t_start_waveforms, // start time of each waveform
    const float* gains,
    // SiPM details
    const float* xt, // cross-talk of each pixel
    const float* std_ucells, // ucells gain dispersion of each pixel
    const int* mask, // pixel mask
    // Background
    const float* inv_bkg_rate, // inverse of the background rate for each pixel
    float bkg_start, // time from which generate backgorund
    float bkg_end, // time at which stop background generation
    // Random seed
    unsigned long long* seed, // seed for each pixel
    // Number of pixels
    int n_pixels
)
{
    // Current block
    int bid = blockIdx.x;

    // A block for each pixel channel -> n_pixels*n_channels blocks
    if (bid > __mul24(n_channels, n_pixels) - 1) return;

    // Channel assigned to this block
    int channel = bid / n_pixels;

    if (skip_channel[channel]) return;

    // Pixel assigned to this block
    int pixel_id = bid - n_pixels * channel;

    // Current channel window length
    int n_window = windows_map[channel+1] - windows_map[channel];

    // Pointer to the current channel signal
    float* y = &signals[signals_map[channel]];

    // Pointer to the current channel time-window
    const float* t = &windows[windows_map[channel]];

    // Shared memory allocation
    // The size is dictated by the wider window:
    //    shared_mem_size = (max_window_size+n_threads*2 + 32) * sizeof(float)
    extern __shared__ float shared_mem[];

    // Pointer to the shared channel signal
    float* sm_signal = shared_mem;

    // Pointers for batch queues
    float* queue_t = (float*)&sm_signal[n_window]; // Generated times
    float* queue_amp = (float*)&queue_t[blockDim.x]; // Generated amplitudes
    float* scan_temp = (float*)&queue_amp[blockDim.x]; // Temporary array for cumulative time

    // Initialize shared signal to 0
    for (int i = threadIdx.x; i < n_window; i += blockDim.x) {
        sm_signal[i] = 0.0f;
    }

    // Write into global memory zero-filled waveforms for masked pixels
    if (mask[pixel_id] == 1) {
        for (int i = threadIdx.x; i < n_window; i += blockDim.x) {
             y[__mul24(pixel_id, n_window) + i] = 0.0f;
        }
        return;
    }

    // RNG initialization for each thread
    curandStatePhilox4_32_10_t state;
    curand_init(seed[pixel_id], 0, 0, &state);

    // Load constants to registers
    float local_xt = xt[pixel_id];
    float local_std_ucells = std_ucells[pixel_id];
    cudaTextureObject_t current_waveform_texture = textures[channel];
    float inv_dt_waveform = inv_dt_waveforms[channel];
    float t_start_waveform = t_start_waveforms[channel];

    // Loop over source photo-electrons arrival time
    // Note:
    //    For IACT simulation the majority of the events have few Cherenkov photons.
    //    So, the part that needs to be accelerated is the background simulation (the while loop).
    //    I am not sure if applying the same batch logic here will help.
    //
    int j_start = map[pixel_id];
    int j_end = map[pixel_id+1];
    for (int j=j_start; j<j_end; j++)
    {
        // Get arrival time index
        float t0 = t0s[j];

        // Number of cross-talk photo-electrons
        float n_xt = borel_generator(local_xt, state);

        // Add micro-cells gain dispersion
        float xt_pe = waveform_normalization(state, n_xt, local_std_ucells);
        
        for (int i = threadIdx.x; i < n_window; i += blockDim.x) {
            float tdiff = t[i] - t0;

            // Skip time-slice if it is before the arrival time
            if (tdiff < 0.0f) continue;

            // Update the waveform
            float single_waveform = interp1d_text(
                tdiff,
                inv_dt_waveform,
                t_start_waveform,
                current_waveform_texture
            );
            sm_signal[i] += single_waveform * xt_pe;
        }
    }
    
    // Each thread generates different background events, so it needs its own RNG state
    curand_init(seed[pixel_id], threadIdx.x, 0, &state);

    // Load constants to registers
    float local_inv_bkg_rate = inv_bkg_rate[pixel_id];
    float current_batch_start_time = local_inv_bkg_rate > 1e6f ? bkg_end + 1.f : bkg_start;

    /////// Batched background loop ///////
    while (current_batch_start_time < bkg_end) {
        
        // Each thread generates:
        //    - a poisson inter-arrival time
        //    - the number of borel discharge
        //    - the gain of the micro-cell
        float pe_dt = poisson_interarrival_time(state, local_inv_bkg_rate);
        float pe_n_xt = borel_generator(local_xt, state);
        float pe_amp = waveform_normalization(state, pe_n_xt, local_std_ucells);

        // Parallel prefix sum to get the correct time for this thread
        float total_dt = block_prefix_sum(pe_dt, scan_temp);
        float batch_t = current_batch_start_time + total_dt;

        // Store the time generated by this thread
        queue_t[threadIdx.x] = batch_t;
        queue_amp[threadIdx.x] = pe_amp;
        
        // Wait untile all times are generated
        __syncthreads();

        // Update the while loop (latest time at the last thread id)
        float last_time = queue_t[blockDim.x - 1]; 
        current_batch_start_time = last_time;

        // Iterate through all the generated times
        // now that they are visibile to all threads
        for (int k = 0; k < blockDim.x; k++) {
            float t_noise = queue_t[k];
            float xt_pe = queue_amp[k];

            if (t_noise > bkg_end) break;

            // Update the waveform
            for (int i = threadIdx.x; i < n_window; i += blockDim.x) {
                float tdiff = t[i] - t_noise;

                if (tdiff < 0.0f) continue;

                float single_waveform = interp1d_text(
                    tdiff,
                    inv_dt_waveform,
                    t_start_waveform,
                    current_waveform_texture
                );
                sm_signal[i] += single_waveform * xt_pe;
            }
        }
        __syncthreads();
    }

    // Write back to global memory
    float local_gain = gains[bid];
    for (int i = threadIdx.x; i < n_window; i += blockDim.x) {
        y[__mul24(pixel_id, n_window) + i] = sm_signal[i] * local_gain;
    }
}

} // extern C