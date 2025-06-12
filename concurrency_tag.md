## Lock Types
- sync::mutex::Mutex
- sync::rwlock::RwLock
- sync::rwmutex::RwMutex
- sync::spin::SpinLock

## Lock API
- sync::spin::SpinLock::<T, G>::lock
- sync::spin::SpinLock::<T, G>::lock_arc
- sync::rwlock::RwLock::<T>::read
- sync::rwlock::RwLock::<T>::read_arc
- sync::rwlock::RwLock::<T>::write
- sync::rwlock::RwLock::<T>::write_arc
- sync::mutex::Mutex::<T>::lock
- sync::mutex::Mutex::<T>::lock_arc
- sync::rwmutex::RwMutex::<T>::read
- sync::rwmutex::RwMutex::<T>::write
- sync::rwmutex::RwMutex::<T>::upread

## ISR
- arch::x86::iommu::fault::iommu_page_fault_handler
- arch::x86::kernel::tsc::determine_tsc_freq_via_pit::pit_callback
- arch::x86::serial::handle_serial_input
- arch::x86::timer::apic::init_periodic_mode::pit_callback
- arch::x86::timer::timer_callback
- smp::do_inter_processor_call
- mm::tlb::do_remote_flush
- log::Log::log

## Panic
- panicking::panic_handler

## Interrupt API
- arch::x86::irq::enable_local
- arch::x86::irq::disable_local