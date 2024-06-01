# Chapter 2

Processor status flags: **manage states** (core state, special state, or supervisor state) and **user states** (target state, normal state, or user state).
When the processor is in the manage state, the program can execute all instructions and use all resources. When it is in the user state, it can only execute non-privileged instructions.

## Processor States

The processor transitions from the user state to the kernel state in the following cases:

- The program requests an operating system service and performs a system call.
- During program execution, an interrupt or exception event occurs, interrupting the running program and transferring control to the interrupt or exception handler.

Both cases occur through the interrupt mechanism. Interrupts and exceptions are the only ways to transition from user state to kernel state.

**User Stack**: An area allocated in the user process space used to store parameters, return values, return addresses, and local variables of subroutines (functions) called by the application program.

**Kernel Stack**: A region in the operating system space used to store interrupt contexts and parameters, return values, return addresses, and local variables of inter-process calls to the operating system.

**Stack Pointer**: The hardware stack pointer that is shared between the user stack and the kernel stack.

Operating systems introduce a program status word **PSW (Program Status Word)** to differentiate between different processor operating states.

- The PSW is used to control the order of instruction execution and to preserve and indicate system states related to the program. Its main purpose is to protect and restore program states.
- Each program has its own PSW associated with its execution, and each processor has a PSW register. When a program occupies the processor for execution, its PSW occupies the PSW register.

The PSW register includes the following contents:

- Program basic states:
    1. Program counter.
    2. Condition codes.
    3. Processor status bits.
- Interrupt code: Saves the current interrupt event that occurred during program execution.
- Interrupt mask: Indicates whether to respond to the interrupt event that occurs during program execution.

## Interrupt Techniques

Reasons for interrupt techniques:

1. Synchronous operations: Fast CPU working in parallel with slow external devices.
2. Fault handling: Handling emergency events related to machine hardware errors.
3. Real-time processing: Real-time microcomputer control systems used in industrial control.

An interrupt is the process of temporarily suspending the execution of the current program on the CPU and transferring control to the corresponding event handler when an urgent event that needs to be processed is encountered during program execution.
The interrupt system is a component that implements interrupt functionality, including interrupt devices and interrupt handlers.
Interrupt device: Refers to the hardware that detects and responds to interrupts.

- Detects interrupt sources and raises interrupt requests.

- Saves the context.

- Starts the program for handling the interrupt event.

Interrupt handler: Implemented by software.

- The main task is to handle the interrupt event and restore normal operation.
**Difference between Interrupts and Exceptions:**

1. Interrupts: Triggered by interrupt signals that are unrelated to the current instruction being executed (asynchronous), and the occurrence of interrupts is independent of whether the CPU is in user mode or kernel mode. Interrupts can only be responded to between two machine instructions, and in general, the services provided by interrupt handlers are not for the current process; Exceptions: Caused by the current instruction being executed by the processor, and exceptions can be responded to during the execution of an instruction. The services provided by exception handlers are for the current process. Exceptions include many aspects (such as faults and traps).

2. "Interrupts" need to be processed quickly in order to respond to other interrupt signals in a timely manner, so the interrupt handler cannot be blocked during the processing. "Exceptions" are in the context of the interrupted current process, and the services provided are needed by the current process, so the exception handler can be blocked during the processing.

3. Interrupts can occur nested, but exceptions are mostly single-level; exceptions may occur during the processing of interrupts, but interrupts will never be interrupted by exceptions.

Conditions for CPU to respond to interrupts:

1. Set the interrupt request trigger to send an interrupt request signal.
2. Set the interrupt mask trigger. When this trigger is "1", the interrupt request from the external device can be sent to the CPU.
3. CPU is in the interrupt-enabled state.
4. CPU responds to interrupts after the execution of a current instruction.

**Linux Interrupt Vector**
The vectors for non-maskable interrupts and exceptions are fixed, while the vectors for maskable interrupts can be changed by programming the interrupt controller.
256 interrupt vectors are allocated as follows:

1. Vectors `0-31` correspond to exceptions and non-maskable interrupts.
2. Vectors `32-47` correspond to maskable interrupts used by external devices.
3. Vectors `48-255` are allocated to software interrupts.

Interrupt Sources and Interrupt Types in IBM PC/XT
| 8259 Input | Interrupt Number | Interrupt Source      |
| ---------- | ---------------- | --------------------- |

| IRQ0       | 08               | Electronic Clock Timer |
| IRQ1       | 09               | Keyboard Interrupt    |
| IRQ2       | 0A               | Reserved for Users    |
| IRQ3       | 0B               | Asynchronous COM2     |
| IRQ4       | 0C               | Asynchronous COM1     |
| IRQ5       | 0D               | Hard Disk Interrupt   |
| IRQ6       | 0E               | Floppy Disk Interrupt |
| IRQ7       | 0F               | Parallel Printer      |

**Characteristics of Interrupt Handlers:**

1. They run asynchronously and may interrupt the execution of critical code or even other interrupt handlers.
2. They run in the masked interrupt state and, in the worst case, may disable all interrupts.
3. They perform operations on hardware with high timing requirements. They run in the interrupt context, so they cannot be blocked.

## Processes and Their Implementation

Process definition: A process is a computational activity of an executable program on a set of data that can be executed concurrently. It is also the basic unit for resource allocation and protection by the operating system.
A process is a system mechanism that supports program execution and can describe the concurrent execution process of a program.

A process is a system mechanism that supports program execution.

**Process Attributes:**

- Dynamism: A process is the execution process of a program on a set of data, and it is a dynamic concept, while a program is a static concept consisting of an ordered sequence of instructions.
  - A process has a life cycle: creation, execution, waiting, etc.
  - A process has a dynamic address space (quantity and content).
- Sharing: When the same program runs on different data sets, it constitutes different processes.
- Independence: It is the basic unit for resource allocation and protection in the system and the independent unit for system scheduling (single-threaded process). The address space of each process is independent of each other.

- Constraint: There are constraints between concurrent processes, and they need to wait for each other or communicate messages at critical points.
- Concurrency: Each process advances at its own independent and unpredictable speed. Concurrency and asynchronous characteristics lead to the irreproducibility of program execution.
- Sharing: When the same program runs on different data sets, it constitutes different processes.
- Independence: It is the basic unit for resource allocation and protection in the system and the independent unit for system scheduling (single-threaded process). The address space of each process is independent of each other.
- Constraint: There are constraints between concurrent processes, and they need to wait for each other or communicate messages at critical points.
- Concurrency: Each process advances at its own independent and unpredictable speed. Concurrency and asynchronous characteristics lead to the irreproducibility of program execution.

**进程切换上下文的步骤：**

1. 保存被中断进程的处理器现场信息
2. 修改被中断进程的进程控制块有关信息，如进程状态等
3. 把被中断进程的PSW加入有关队列
4. 选择下一个占有处理器运行的进程
5. 修改被选中进程的PSW的有关信息
6. 根据被选中进程设置操作系统用到的地址转换和存储保护信息
7. 根据被选中进程恢复处理器现场

进程阻塞步骤：
步1：停止进程执行，保存现场信息到PCB；
步2：修改进程PCB有关内容，如进程状态由运行态改为等待态等，并把修改状态后的进程移入相应事件的等待队列中；
步3：转入进程调度程序去调度其他进程运行。
进程唤醒步骤：
步1：从相应的等待队列中移出进程；
步2：修改进程PCB的有关信息，如进程状态改为就绪态，并移入就绪队列；
步3：若被唤醒进程比当前运行进程优先级高，重新设置调度标志。

多线程结构进程的优点
1.快速线程切换
2.通信易于实现
3.减少管理开销
4.并发程度提高 


进程是操作系统中除处理器外进行的资源分配和保护的基本单位。
它有独立的虚拟地址空间，容纳进程映像(如与进程关联的程序与数据)，并以进程为单位对各种资源实施保护，如受保护地访问处理器、文件、外部设备及其他进程(进程间通信)。
线程是操作系统进程中能够独立执行的实体（控制流）,是处理器调度和分派的基本单位。
线程是进程的组成部分，每个进程内允许包含多个并发执行的实体（控制流），这就是多线程。

用户级线程的活动
内核不知道线程的活动，但仍然管理线程所属进程的活动；
当线程调用系统调用时，整个进程阻塞；
但对线程库来说，线程仍然是运行状态
即线程状态是与进程状态独立的。


用户级线程优缺点
优点
线程切换不调用内核
调度是应用程序特定的：可以选择最好的算法。
ULT可运行在任何操作系统上（只需要线程库）。
缺点
大多数系统调用是阻塞的，因此核心阻塞进程，故进程中所有线程将被阻塞。
核心只将处理器分配给进程，同一进程中的两个线程不能同时运行于两个处理器上。

内核级线程（KLT）
由操作系统的内核建立、调度和管理的线程。
所有线程管理由内核完成
没有线程库，但对内核线程工具提供API
内核维护进程和线程的上下文
线程之间的切换需要内核支持
以线程为基础进行调度
例子：Windows NT，OS/2

内核级线程的优点及缺点
优点：
对多处理器，内核可以同时调度同一进程的多个线程
阻塞是在线程一级完成
内核例程是多线程的
缺点：
在同一进程内的线程切换调用内核，导致速度下降

调度和切换速度
    ULT切换快， KLT切换与进程切换相似。ULT通常发生在一个应用进程的诸线程中，无需通过中断进入内核。
系统调用
    ULT进行系统调用时，会引起进程的阻塞；KLT进行系统调用时只会引起该线程阻塞。
线程执行时间
    ULT以进程为单位调度，KLT以线程为单位调度。
    ULT：进程A有1个线程，进程B有100个线程，则A的线程比B快
    KLT：进程A有1个线程，进程B有100个线程，则B比A快
使用范围：
    ULT广，任何OS， KLT需OS内核支持
调度算法
    ULT与OS调度算法无关，可针对应用优化
多处理器支持
    KLT可充分利用多处理器


资源利用率
 CPU利用率=CPU有效工作时间/CPU总的运行时间，
 CPU总的运行时间=CPU有效工作时间+CPU空闲等待时间
响应时间
交互式进程从提交一个请求(命令)到接收到响应之间的时间间隔称响应时间。
使交互式用户的响应时间尽可能短，或尽快处理实时任务。
这是分时系统和实时系统衡量调度性能的一个重要指标。
周转时间
批处理用户从作业提交给系统开始，到作业完成为止的时间间隔称作业周转时间，应使作业周转时间或平均作业周转时间尽可能短。
这是批处理系统衡量调度性能的一个重要指标。
吞吐率
单位时间内处理的作业数。
  公平性
确保每个用户每个进程获得合理的CPU份额或其他资源份额，不会出现饿死情况

如果作业i提交给系统的时刻是ts，完成时刻是tf，该作业的周转时间ti为：
                ti = tf - ts
实际上，它是作业在系统里的等待时间与运行时间之和。
为了提高系统的性能，要让若干个用户的平均作业周转时间和平均带权周转时间最小。
          平均作业周转时间 T =(       )/ n

如果作业i的周转时间为ti，所需运行时间为tk，则称wi=ti /tk为该作业的带权周转时间。
ti是等待时间与运行时间之和，故带权周转时间总大于1。
   平均作业带权周转时间W=(       )/ n

作业是任务实体，进程是完成任务的执行实体；没有作业任务，进程无事可干，没有进程，作业任务没法完成。
作业概念更多地用在批处理操作系统，而进程则可以用在各种多道程序设计系统


JCB通常是在批作业进入系统时，由Spooling系统建立的，它是作业存在于系统的标志，作业撤离时，JCB也被撤销。
 JCB的主要内容包括：
作业情况
资源需求
资源使用情况
作业生命周期状态
输入状态
作业被提交给机房后或用户通过终端键盘向计算机中键入其作业时所处的状态。
 后备状态
作业的全部信息都已通过输入设备输入，并由操作系统将其存放在磁盘的某些盘区中等待运行。
 执行状态
作业调度程序选中而被送入主存，并建立进程投入运行。
 完成状态
作业完成其全部运行，释放其所占用的全部资源


第一类称剥夺式：
又称抢占式。当进程/线程正在处理器上运行时，系统可根据规定的原则剥夺分配给此进程/线程的处理器，并将其移入就绪队列，选择其他进程/线程运行。
两种处理器剥夺原则：
高优先级进程/线程可剥夺低优先级进程/线程，
当运行进程/线程时间片用完后被剥夺。
第二类称非剥夺式： 
又称非抢占式。一旦某个进程/线程开始运行后便不再让出处理器，除非该进程/线程运行结束或主动放弃处理器，或因发生某个事件而不能继续执行。


shortest next CPU burst time(1) 
burst--最短下一个CPU突发周期长度 
计算进程/线程下一个CPU周期长度 
                τn+1=αtn+(1-α)τn
tn是进程/线程最近一个CPU周期长度，是最近信息；
τn是估算的第n个CPU周期值，是历史信息。 



  响应比 ＝1+已等待时间/估计运行时间

 短作业容易得到较高响应比，   
 长作业等待时间足够长后，也将获得足够高的响应比，
 饥饿现象不会发生。
