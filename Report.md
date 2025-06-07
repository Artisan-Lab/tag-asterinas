### Asterinas Safety Comment改进思路

#### 抽象状态 => 具体函数

##### Example 1

将抽象系统状态描述**具体化，统一化**，考虑用相关**函数已经发生或未发生**/相关**变量已初始化或未初始化**来代替。

```rust
/// 被调用函数的Safety要求
/// This function should be called only once after the memory regions are ready.
pub(crate) unsafe fn init_early_allocator() {
    let mut early_allocator = EARLY_ALLOCATOR.lock();
    *early_allocator = Some(EarlyFrameAllocator::new());
}

// 调用该函数的Safety解释
// SAFETY: This function is called only once, before `allocator::init` and after memory regions are initialized.
unsafe { mm::frame::allocator::init_early_allocator() };
```

总体来看，调用处的注解仅仅重复了一遍被调用者的要求，并不能依次清晰自明地解释为何能消除unsafe风险，注意到：

- `called only once`实际上可以分解为**上层调用者只被调用一次+不存在其他的路径调用该函数**
- `memory regions are ready`是一个相对模糊的状态描述，从函数内容来看实际上是要求`EARLY_INFO.memory_region`这一**具体变量**已经正确初始化

```rust
// Safety Discharge:
// 1. ★`init()` is the sole caller and is guaranteed to be called once
// 2. ★Called after memory regions (in EARLY_INFO) are initialized
unsafe { mm::frame::allocator::init_early_allocator() };
```

##### Example 2

```rust
pub unsafe fn activate_kernel_page_table() {
    let kpt = KERNEL_PAGE_TABLE
        .get()
        .expect("The kernel page table is not initialized yet");
    // SAFETY: the kernel page table is initialized properly.
    unsafe {
        kpt.first_activate_unchecked();
        crate::arch::mm::tlb_flush_all_including_global();
    }
    // SAFETY: the boot page table is OK to be dismissed now since the kernel page table is activated just now.
    unsafe {
        crate::mm::page_table::boot_pt::dismiss();
    }
}
```

修改为

```rust
pub unsafe fn activate_kernel_page_table() {
    let kpt = KERNEL_PAGE_TABLE
        .get()
        .expect("The kernel page table is not initialized yet");
    // Safety Discharge:
    // ★Called after KERNEL_PAGE_TABLE is initialized
    unsafe {
        kpt.first_activate_unchecked();
        crate::arch::mm::tlb_flush_all_including_global();
    }

    // Safety Discharge:
    // ★Called after KERNEL_PAGE_TABLE is activated (first_activate_unchecked)
    unsafe {
        crate::mm::page_table::boot_pt::dismiss();
    }
}
```

#### 职权混乱 => 厘清层次

在safety能够被**确保履行**的位置进行注释，无法根据上下文消去的unsafe需要被**传播**到上层函数

```rust
/// The caller must ensure that
/// 1. We're in the boot context of the BSP and APs have not yet booted.
/// 2. The number of available processors is available.
/// 3. No CPU-local objects have been accessed.
pub(crate) unsafe fn init_on_bsp() {
    let num_cpus = crate::arch::boot::smp::count_processors().unwrap_or(1);

    // SAFETY: The safety is upheld by the caller and the correctness of the `get_num_processors` method.
    unsafe {
        local::copy_bsp_for_ap(num_cpus as usize);
        set_this_cpu_id(0);
        init_num_cpus(num_cpus);
    }
}
```

- 这里`num_cpus`是由一个**safe**函数生成的，但实际上是作为一个带有unsafe风险的参数被后续函数调用。因此`count_processors()`需要被改为一个unsafe函数
- 同时对于ACPI table的安全要求并不能在上下文中体现，因此需要传播到`init_on_bsp()`
- 同样，下方unsafe函数的部分要求也需要传播到`init_on_bsp()`【实际上已经注明】
- `set_this_cpu_id(0)`的unsafe能够被上下文推导直接消除

```rust
/// # Safety
///
/// The caller must ensure that
/// 1. We're in the boot context of the BSP and APs have not yet booted.
/// 2. ★This function needs to be called after the OS initializes the ACPI table.
/// 3. No CPU-local objects have been accessed.
pub(crate) unsafe fn init_on_bsp() {
    unsafe {
        let num_cpus = crate::arch::boot::smp::count_processors().unwrap_or(1)
        local::copy_bsp_for_ap(num_cpus as usize);
        // Safety Discharge:
        // ★We're in the boot context of BSP, thus the current id is 0.
        set_this_cpu_id(0);
        init_num_cpus(num_cpus);
    }
}

/// Safety:
/// ★This function needs to be called after the OS initializes the ACPI table.
pub(crate) ★unsafe fn count_processors() -> Option<u32> {

/// Safety:
/// ★This function needs to be called after the OS initializes the ACPI table.
pub(crate) ★unsafe fn get_acpi_tables() -> Option<AcpiTables<AcpiMemoryHandler>> {
```

#### 有漏待补 => 查漏补缺

部分unsafe函数在调用处消除了风险但没有标注

```rust
unsafe { arch::late_init_on_bsp() };
```

修改为

```rust
// Safety Discharge:
// 1. `init()` is the sole caller and is guaranteed to be called once
// 2. Called in BSP boot context
unsafe { arch::late_init_on_bsp() };
```

### Tag Asterinas

- CallOnce
- Initialized(obj)
- PriorTo(func)
- NeverAccess(mem)
- ValidCtx
- ……