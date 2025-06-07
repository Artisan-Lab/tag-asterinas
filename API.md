mm::frame::allocator::init_early_allocator

This function should be called only once after the memory regions are ready.

- CallOnce
- Fulfilled(EARLY_INFO)

init_on_bsp

/// 1. We're in the boot context of the BSP and APs have not yet booted.
/// 2. The number of available processors is available.
/// 3. No CPU-local objects have been accessed.

- Unfulfilled(AP_start)
- Fulfilled(EARLY_INFO)
- ?

/// This function must be called in the boot context of the BSP, at a time
/// when the APs have not yet booted.
///
/// The CPU-local data on the BSP must not be used before calling this
/// function to copy it for the APs. Otherwise, the copied data will
/// contain non-constant (also non-`Copy`) data, resulting in undefined
/// behavior when it's loaded on the APs.
///
/// The caller must ensure that the `num_cpus` matches the number of all
/// CPUs that will access the CPU-local storage.
copy_bsp_for_ap
- Fulfilled(BSP_start) & Unfulfilled(BSP_end) & Unfulfilled(AP_start)
- Unmodified(BSP_region_start, BSP_region_end)
- ValidNum(cpu)

/// # Safety
///
/// This method must be called on each processor during the early
/// boot phase of the processor.
///
/// The caller must ensure that this function is called with
/// the correct value of the CPU ID.
set_this_cpu_id
- UnFulfilled(AP_end) || UnFulfilled(BSP_end)
- ValidCpuId(id)

init_num_cpus()

/// 1. We're in the boot context of the BSP and APs have not yet booted.
/// 2. The argument is the correct value of the number of CPUs (which
///    is a constant, since we don't support CPU hot-plugging anyway).
- Fulfilled(BSP_start) & Unfulfilled(BSP_end) & Unfulfilled(AP_start)
- ValidNum(cpu)



