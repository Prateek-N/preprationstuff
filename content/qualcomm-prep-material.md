# Qualcomm NPU / Embedded Platform Interview Prep

This file combines role-level/system prep and specific coding-question patterns for Qualcomm NPU / embedded platform software engineer roles.

## 1. Role and Interview Structure

Qualcomm NPU / AI platform software engineers work on embedded platform software for CPU, DSP, and NPU blocks in Snapdragon SoCs, building execution environments, IPC, memory management, and frameworks that accelerate ML, CV, multimedia, and sensor workloads.

Typical onsite/virtual-onsite loop (after recruiter screen):

- 4–6 technical rounds (45–60 minutes each).
- Mix of C/C++ coding, OS & concurrency, embedded/RTOS & drivers, SoC/IPC design, low-level debugging, and ML/DSP workload mapping.
- 1 behavioral / project deep-dive or lunch-style conversation.

High-level round themes:

- **Round 1:** C / C++ fundamentals and memory (pointer-heavy coding, small DS problems).
- **Round 2:** OS, concurrency, and IPC (threads, scheduling, deadlocks, mutex vs semaphore, classic sync problems).
- **Round 3:** Embedded / RTOS / drivers (interrupts, DMA, MMU basics, memory-mapped I/O, user→kernel path).
- **Round 4:** System / firmware design + debugging (timer modules, queues, power management, bring-up issues).
- **Round 5:** NPU / DSP / ML-platform flavored round (mapping CNN/CV workloads to CPU/DSP/NPU, quantization, performance & power).
- **Behavioral:** debugging stories, cross-team collaboration, ownership and system-level thinking.


## 2. Core Technical Topic Buckets

### 2.1 C / C++ for Embedded

What they emphasize:

- Pointers and memory layout: pointer arithmetic, arrays vs pointers, function pointers, pointer-to-function-returning-pointer; text/data/bss/heap/stack; lifetime of auto/static/global/const/volatile variables.
- Implementing libc-style functions: `memcpy`, `memmove`, `strstr`, `strcmp`, string reverse, strtok-like parsing, etc.
- Linked-list and tree manipulation in plain C: reverse list, detect loop, length of loop, intersection point of two lists, list→BST, tree traversals.
- Bit manipulation: reverse bits, count set bits, power-of-two checks, masking/unmasking register fields.
- Undefined behavior and safety: dangling pointers, double free, out-of-bounds access, strict aliasing.

Level: LeetCode Easy–Medium for most questions; occasional Medium–Hard when they mix in constraints or ask for optimized implementations.

### 2.2 Embedded Memory, MMU, and Performance

Expect to talk like a systems/performance engineer:

- Stack vs heap: when to avoid dynamic allocation, stack overflow scenarios (deep recursion, large arrays), detection and prevention.
- Static allocation and memory pools: fixed-size pools, moving constants to flash/ROM.
- Alignment and caches: why alignment matters for performance and DMA; cache-coherency for shared memory between cores or with DMA; memory barriers.
- MMU basics: page tables, sections vs pages, attributes, debugging MMU enable freezes on bring-up.
- Optimization: minimizing copies, streaming I/O, using profiling to improve performance/memory/power.


### 2.3 OS, RTOS, and Concurrency

Key OS/RTOS fundamentals they probe:

- Processes vs threads, context switching, user vs kernel mode, system-call path.
- Scheduling: round-robin, priority-based, real-time basics.
- Deadlocks: the four conditions, detection, prevention/avoidance.
- Sync primitives: mutex, binary vs counting semaphore, spinlocks, condition variables, readers–writer locks; priority inversion and priority inheritance.
- Interrupts and ISRs: top-half vs bottom-half, writing ISRs that are short/non-blocking, deferring work to threads.


### 2.4 Inter-Processor Communication & Heterogeneous SoCs

The JD explicitly highlights IPC and execution environments across CPU, DSP, and NPU.

- IPC mechanisms on SoC: shared-memory queues/ring buffers, mailboxes, message queues, doorbell interrupts.
- Cache-coherent vs non-coherent regions and how to handle cache maintenance for shared buffers.
- Designing CPU↔NPU/DSP protocols: descriptors, command queues, completion events, error codes, timeouts.
- Latency vs throughput vs power trade-offs when batching work.


### 2.5 Drivers and Peripherals

They often test user–kernel boundaries and peripheral basics:

- System-call path: what happens on a `read()`/`write()` to a device.
- Character vs block devices; driver initialization, probe, and teardown.
- Memory-mapped I/O; programming device registers, handling status bits and interrupts.
- I2C/SPI/UART: transaction sequences, clock stretching, arbitration, error handling.
- DMA: configuring DMA, ensuring buffers are correctly aligned and visible, interaction with caches/TLB.


### 2.6 Debugging, Trace32, JTAG

Debugging mindset is critical:

- JTAG basics: connecting to target, setting breakpoints and watchpoints, single-stepping, inspecting registers/memory.
- Using Trace32 or similar to debug hangs, crashes, and boot failures.
- Debugging scenarios: MMU bring-up issues, memory leaks, stack corruption, and protocol glitches using a combination of logging, watchpoints, and logic analyzers.


### 2.7 DSP / Hexagon and ML Workloads

Depending on team, expect some DSP/ML flavor:

- DSP concepts: fixed-point (Q-format), overflow, saturation, FIR/IIR filters, convolution, FFT; why DSPs exist vs CPUs.
- ML/CV workload view: convolutions, matmul, activations, pooling; high-level understanding of CNNs (ResNet/VGG/Inception) as compute graphs.
- Systems angle: quantization (e.g., int8), partitioning workloads across CPU/DSP/NPU, and how that affects latency, power, and memory.


### 2.8 Testing and Automation

Preferred skills mention scripting (Python/shell) and test automation.

- Unit tests, integration tests, and HIL tests for firmware/drivers.
- Python or shell scripts for flashing, running regression suites, log scraping.
- Designing logging and tracing hooks to make field debugging tractable.


### 2.9 Behavioral and Project Deep-Dives

Behavioral is technical-story heavy:

- Tough debugging story: hypothesis→experiments→root cause→fix.
- Cross-team collaboration with hardware/firmware/test; handling conflicting priorities.
- Performance/memory/power trade-offs made under pressure.


## 3. Coding Problems & Levels

### 3.1 Overall Coding Difficulty

From OA and onsite reports, Qualcomm coding is mostly LeetCode Easy–Medium with some Medium–Hard problems, especially for OA or DSP/ML-heavy teams.

- OA (HackerRank-style): 6–10 Easy/Medium questions + MCQs on C/DS/OS; very rarely a Hard problem.
- Onsite rounds: 1–2 coding problems per round, mostly Medium, wrapped in system/embedded context.


### 3.2 High-Frequency Coding Topics

#### Linked Lists (very high frequency)

Questions seen repeatedly in Qualcomm-specific lists and experiences:

- Reverse a singly linked list – Easy.
- Reverse a doubly linked list – Easy–Medium.
- Detect loop in a linked list (Floyd cycle) – Medium.
- Find length of loop – Medium.
- Intersection point of two singly linked lists – Medium.
- Convert a sorted linked list to BST – Medium.


#### Trees / Graphs

Typical Medium-level problems:

- Check if a binary tree is a BST.
- Left view of a binary tree.
- Minimum distance between two nodes in a binary tree.
- Graph traversal (DFS/BFS) on adjacency list/matrix; appears in ML/system engineer rounds.


#### Strings / Arrays

Found across Qualcomm coding archives and experiences:

- Implement `strstr` (find substring) – Medium; asked with a request for an optimal approach.
- Implement `memcpy` / `memmove` with overlap handling and alignment hints – Medium–Hard.
- Reverse a string without library calls – Easy.
- Check if one array is a subset of another – Medium.
- Rotate array by k positions – Easy–Medium.
- Find missing number in 1..n – Easy–Medium.
- Count pairs (a, b) such that (a + b) is divisible by k – Medium; seen in Sr Engineer/AI interviews.
- Misc pattern-printing / math problems (e.g., hollow pyramid, counting squares on a chessboard) – Easy.


#### Bit Manipulation / Math

Classic embedded-style C questions:

- Reverse bits of an integer – Medium.
- Count set bits – Easy–Medium.
- Check power of two – Easy; usually expect a bit trick.
- Toggle specific bits using masks – Easy.


#### Hashing, Stacks, Queues

DS fundamentals checked in ML/system engineer rounds:

- Intersection of two linked lists using a hash set/map.
- Basic stack/queue implementations and usage for expression evaluation/parentheses check/level-order traversal.


#### Harder / Domain-Flavored Problems (less frequent)

From DSP SWE and ML/system engineer experiences:

- Compression with deletions: given a string and max deletions k, minimize compressed length (run-length-style encoding) – Medium–Hard.
- Grid optimization: choose squares in a grid to maximize coverage under constraints – Medium–Hard (DP/greedy).
- C code for a small backpropagation step in a CNN – Hard, ML-specific.
- Bitstream error detection / simple channel coding logic in C – Medium–Hard.


### 3.3 Stage vs Difficulty Summary

| Stage / Type | Difficulty mix | Notes |
| :-- | :-- | :-- |
| OA (HackerRank) | Mostly Easy–Medium, rare Medium–Hard | 6–10 coding Qs + C/DS/OS MCQs |
| Phone / first tech | Easy–Medium | Linked lists, arrays, strings, bits |
| Later onsite tech (2–4 rounds) | Mainly Medium, a few Easy/Medium–Hard | More system context, trees/graphs, libc re-impl |
| DSP/ML/system heavy teams | Medium–Hard for 1–2 problems | Compression/grid/backprop/bitstream tasks |

## 4. Recommended Prep Plan (Tailored)

Given strong backend/microservices/Algo-trading background, focus is on closing embedded, C, and SoC gaps rather than basic problem-solving.

### 4.1 Coding Practice Focus

- Grind LeetCode / GFG problems in the following order:
    - Linked lists → strings & arrays → bit manipulation → trees/graphs (traversals, views, distances).
    - Re-implement `memcpy`, `memmove`, `strstr`, `strcmp`, string reverse, etc., in C.
- For each problem, explain pointer behavior and memory layout out loud; Qualcomm cares about reasoning, not just passing testcases.


### 4.2 Systems & Embedded Focus

- OS/RTOS: revise using OS lecture notes or a good embedded-OS blog; drill deadlocks, scheduling, and synchronization with examples.
- Memory & MMU: read an ARM/SoC bring-up post on enabling MMU, TLB, and caches; practice explaining what can go wrong.
- IPC & SoC: model CPU/DSP/NPU subsystems like microservices communicating through shared-memory queues and interrupts.


### 4.3 Story and Behavioral Prep

- Prepare 3–4 strong stories:
    - One major debugging incident (ideally from trading/microservices) with hypothesis→experiments→root cause.
    - One performance optimization (latency/throughput) story.
    - One cross-team alignment/conflict-resolution story.
    - One failure/learning story.
- Translate each to embedded/System-on-Chip language when you narrate it (think latency budgets, resource constraints, HW/SW boundaries).


## 5. Quick Checklist Before Onsite

- Comfortable writing: reverse list, detect loop, `strstr`, `memcpy`, rotate array, bit manip in C.
- Can explain: context switch, deadlock, mutex vs semaphore, priority inversion, ISR rules, MMU basics, DMA + cache coherency.
- Have a mental model of: CPU/DSP/NPU execution environments, shared-memory queues, doorbell interrupts, batching vs latency.
- Can walk through at least one serious debugging story end-to-end.

If you can do all of the above while speaking clearly and drawing diagrams when needed, you are in very strong shape for this Qualcomm NPU / embedded platform onsite.

---

# Qualcomm NPU / Embedded Interview Answers – Aligned to **Vaishnavi Mysore**

## Answer 1 – Real-time Embedded Background

My core strength is building **real-time embedded software** in **C** and **C++** on **ARM Cortex-M** platforms for safety-critical automotive systems. At **General Motors**, I owned application software for **bare-metal** distributed controllers and integrated it across four subsystems, which maps closely to Qualcomm's heterogeneous **SoC** environment where different cores must cooperate predictably. Working with **CAN FD** and **UDS diagnostics** on multi-node networks taught me to reason about timing, bandwidth, and error handling under strict latency budgets. That experience transfers well to coordinating workloads across **CPU**, **DSP**, and **NPU** where throughput and determinism are equally important.

I routinely optimized memory using **linker scripts**, **stack analysis**, and low-level debugging via **JTAG**, reclaiming **48 KB** of usable memory to host additional control logic. On the validation side, my **Vector CANoe** and **CAPL**-driven test harness executes **180+ integration scenarios per build** and has caught **35+ critical defects** before system-level testing. Reducing diagnostic session failures by **22 instances per release cycle** directly demonstrates the impact of rigorous protocol-level testing. This end-to-end view — from signal integrity on the bus to software behavior in the ECU — matches Qualcomm's expectation that platform engineers own their subsystem deeply.

Across both **General Motors** and **Robert Bosch**, I worked within **ISO 26262**, **MISRA C**, and **ASPICE** processes, which enforced disciplined requirements tracing, code quality, and regression coverage. That background helps me write robust platform software and collaborate effectively with hardware and systems teams. Overall, the combination of **device drivers**, **bootloader and OTA**, **AUTOSAR RTE/CDD**, and distributed network experience gives me a strong foundation to contribute to Qualcomm's **NPU platform software** and embedded frameworks.

## Answer 2 – Debugging with JTAG and Low-Level Tools

A representative debugging example that aligns with Qualcomm's expectations involved a **stack overflow** on an **ARM Cortex-M**-based controller at **General Motors**. The system would intermittently reset during high-load diagnostic sessions over **CAN FD** and **UDS**, with no obvious software error. I used **linker scripts** and **map-file** inspection to estimate stack usage for each task, then enabled additional guard zones and stack pattern fills. Using **JTAG** and an **oscilloscope** to monitor reset lines, I captured the exact moment of failure and inspected stack memory to confirm corruption of return addresses.

Once I had evidence of stack overrun, I refactored the **C** routines that combined complex diagnostic state machines and large local buffers. I moved large arrays to statically allocated **.bss** sections, reduced recursion, and split logic into smaller, iterative functions. I also tuned task priorities and reduced worst-case nesting depth in the scheduler. After these changes, we eliminated the resets and recovered around **48 KB** of usable memory, enabling new control features without hardware changes.

In another case at **Robert Bosch**, I debugged a sporadic latency spike in **GNSS** signal processing on a VMPS automotive platform. Using **UART**, **SPI**, and **CAN** traces in **Vector CANoe** plus firmware logging, I correlated the issue with a specific interrupt storm from a noisy peripheral — a burst of 50–80 SPI interrupts in under 1 ms was consuming 70% of CPU time. I adjusted interrupt priorities, shortened ISRs, moved data reassembly to a background task, and recommended an RC filter to the hardware team. The result was a **12 ms reduction in average sensor latency** and **18 hours of debugging time saved per release cycle** through better instrumentation and logging. This combination of measurement, hypothesis, and verification is the same approach I would use with tools like **Trace32** or Qualcomm's internal debuggers to isolate MMU, cache, or IPC issues on **Snapdragon**.

## Answer 3 – Communication Protocols and Inter-Module Integration

Most of my career has been spent designing and validating communication across **distributed ECUs**, which aligns with Qualcomm's emphasis on **inter-processor communication** between **CPU**, **DSP**, and **NPU**. At **General Motors**, I implemented **CAN FD** and **UDS**-based communication for **15+ distributed nodes**, reduced **diagnostic session failures by 22 per release cycle**, and validated **180+ integration scenarios per build** using **Vector CANoe** and **CAPL** scripting. My DBC message layout design and CAPL-based test nodes simulate all peer ECUs simultaneously — including fault injection for bus-off, missing messages, and out-of-sequence frames.

This experience maps conceptually to building shared-memory protocols or message queues between cores in a Snapdragon **SoC**. UDS session management and periodic messaging taught me to design state machines that survive timeouts, retries, and partial failures without locking up the system. On the **Bosch** side, I configured **UART**, **SPI**, and **CAN** interfaces for **GNSS** receivers across **5+ vehicle platforms**, improved signal integrity across **120+ validation scenarios**, and reduced debugging time by **18 hours per release** through better instrumentation and logging.

Because I routinely authored diagnostic and communication requirements aligned with **ISO 26262** and **ASPICE**, I am comfortable defining contracts between components and ensuring traceability. That is directly useful when specifying APIs and protocols for CPU ↔ accelerator interaction, including error codes, watchdog behavior, and performance monitoring. My existing toolset—**CANoe**, **CAPL**, **HIL/SIL**, and **Linux** scripting—also helps me quickly build realistic test harnesses for Qualcomm's **NPU platform software** to simulate load, faults, and corner cases.

## Answer 4 – Bootloaders, OTA, and Firmware Integrity

In my current role at **General Motors**, I implemented and enhanced **bootloader** and **OTA update** mechanisms for automotive ECUs, which is highly relevant to Qualcomm's emphasis on robust platform software. I worked on **secure flashing** workflows, ensuring that firmware images were authenticated and verified before execution, and that rollback paths were clearly defined. Over nine consecutive releases, these mechanisms delivered zero rollback failures, which shows the stability of our design and process.

Technically, this involved writing **Embedded C** code that executed from a minimal startup context on **ARM Cortex-M**, managing flash drivers, checksum or hash verification, and watchdog-safe timing. I coordinated with hardware teams to understand memory layouts and protection regions, and with systems engineers to define update states and failure-handling strategies. On the tooling side, I integrated these flows into **Linux-based** validation environments and **Vector CANoe** test benches, using **UDS** routines to trigger and monitor updates over **CAN FD**.

My earlier experience at **Robert Bosch** with **GNSS** firmware integration gave me a strong foundation in repeatable regression testing for firmware updates — I ran **250+ Python-based regression scenarios per cycle** in virtual validation environments, maintaining build stability across **6 production releases**. I also achieved **3 consecutive ASPICE audit clearances with zero non-conformities** by maintaining strict requirements traceability for safety artifacts. Combining that depth of process discipline with hands-on Embedded C expertise, I always treat bootloader and OTA code as safety- and reliability-critical. At Qualcomm, I can bring the same mindset to any low-level **NPU** boot, secure firmware loading, or field-update mechanisms, ensuring that accelerators come up reliably and can be updated without impacting user devices.

---

## Answer Sheet – Common Interview Q&A (Vaishnavi Mysore)

> Practice these out loud. Each answer is calibrated to 90–120 seconds spoken. Numbers are pulled directly from your resume — don't round or soften them in the interview.

---

### Q1: "Tell me about yourself" (2-minute pitch)

I have four-plus years of hands-on embedded systems experience across two roles — at **Robert Bosch** in India and currently at **General Motors** in the US, with a **Master's in Information Systems and Technology from Wilmington University** completed in December 2024 bridging the two.

At Bosch, I built low-level **Embedded C device drivers** for **GNSS receivers** in VMPS automotive systems, worked across **UART, SPI, and CAN** interfaces across **5+ vehicle platforms**, and achieved a **12 ms reduction in sensor latency**. I also architected **AUTOSAR RTE and CDD** components across **8 control units with zero critical integration defects** across **6 production releases**.

At **General Motors**, I joined as an Embedded Systems Engineer on **bare-metal ARM Cortex-M** platforms. I own C/C++ application software for distributed real-time control systems, implemented **CAN FD and UDS** communication across **15+ nodes** — reducing **diagnostic session failures by 22 per release cycle** — and used linker scripts and JTAG to reclaim **48 KB of memory**. I've built and maintained the **bootloader and OTA update mechanism**, achieving **zero rollback failures across 9 consecutive releases**.

What draws me to Qualcomm is that the NPU platform role is a direct evolution of what I've been doing — instead of coordinating firmware across distributed ECUs over a CAN bus, I'd be coordinating workloads across **CPU, DSP, and NPU cores** over shared-memory queues and doorbell interrupts. The problems are structurally the same: real-time execution, IPC protocols, memory constraints, and debugging at the hardware-software boundary. I'm excited to apply that expertise at Snapdragon scale.

---

### Q2: "Why Qualcomm? Why this NPU/embedded platform role specifically?"

Qualcomm is where embedded software meets the most interesting silicon in the industry. The NPU platform role is not just another embedded job — it's the execution substrate for every on-device AI feature on Snapdragon, and I want to work at that layer.

My background maps directly to the JD. I've spent four years building IPC-heavy firmware across distributed nodes — message layouts, error handling, timing guarantees, JTAG debugging. At the SoC level, those same skills apply to shared-memory command queues, doorbell interrupts, and CPU↔NPU descriptor protocols. I've worked with **AUTOSAR's layered execution environment model**, which is architecturally analogous to how Qualcomm structures platform software for heterogeneous compute. And I've done detailed memory budget analysis with linker scripts and stack profiling — directly applicable to NPU on-chip memory hierarchies.

My Master's degree gave me formal exposure to system-level design and data-flow modeling, which complements my implementation depth.

The combination of Qualcomm's technical depth, the Hexagon DSP and NPU ecosystem, and the opportunity to work on software that ships in hundreds of millions of devices is exactly the right next step for me.

---

### Q3: "Walk me through your most significant technical achievement"

The one I'm most proud of at GM is tracking down and eliminating a stack overflow that was causing intermittent resets on a production ARM Cortex-M controller.

The system would reset roughly once every four hours of diagnostic testing over CAN FD — no fault codes, no obvious error. My first hypothesis was stack overflow because the resets correlated with high-load diagnostic scenarios. I reviewed linker map files, found stack sizes were set by convention rather than measurement, then enabled pattern fills (0xDEADBEEF) across all tasks. The next reset: JTAG post-mortem showed the pattern completely overwritten at the diagnostic task's stack limit.

I set a JTAG watchpoint on the guard region and reproduced the failure in 45 minutes. Root cause: a 2 KB local buffer inside a deeply nested diagnostic state machine, combined with recursive CAN frame parsing, was overrunning a 4 KB allocation.

Fix: moved the buffer to static .bss, flattened the recursion, added an MPU guard page as a permanent tripwire. Result: **zero resets in 200+ hours of subsequent validation**, **48 KB of memory recovered** across four tasks, and the fix landed two days before the validation cycle started. That incident also changed our team's process — stack watermark review is now a standard gate for every release.

---

### Q4: "What is your ARM Cortex-M experience? What have you built on it?"

At GM I build bare-metal application software on Cortex-M. My work spans four areas:

**Application logic:** C/C++ control code across four distributed subsystems, with task priorities and timing managed through our RTOS scheduler.

**Memory and debugging:** I use linker scripts to explicitly control section placement — code in flash, constants in .rodata, critical buffers in specific SRAM regions. JTAG is a daily tool: breakpoints, watchpoints, map-file inspection, stack watermarks. This discipline let me reclaim **48 KB** by fixing a stack overflow that had gone undetected for months.

**Communication:** CAN FD and UDS driver-level work — frame parsing, DBC message layouts, diagnostic session state machines with timeout and retry logic — across **15+ nodes**, reducing session failures by **22 per release**.

**Bootloader:** OTA flashing path — startup code, flash driver, hash verification, watchdog-safe timing. **Zero rollback failures across 9 releases**.

At Bosch, I worked on a different Cortex-M platform for GNSS receivers, building UART, SPI, and CAN drivers and achieving **12 ms latency improvement** by optimizing ISR handling and data path scheduling.

---

### Q5: "How do you approach safety-critical embedded development?"

Both roles operated under **ISO 26262, MISRA C, and ASPICE**, so this discipline is embedded in how I write and review code.

**Process level:** Every requirement traces to a test case. At Bosch, I authored component and functional requirements in ASPICE frameworks, maintained traceability matrices, and achieved **3 consecutive audit clearances with zero non-conformities**. At GM, nine releases under the same discipline.

**Code level:** MISRA C rules are not optional — no dynamic allocation in safety paths, bounded loops, no implicit conversions. I use static analysis as part of the build and treat its findings with the same priority as compiler warnings.

**Test level:** I design tests that exercise failure modes, not just happy paths. My CANoe/CAPL harness at GM covers bus-off conditions, missing nodes, and out-of-sequence frames — **180+ scenarios per build, 35+ critical defects caught before system testing**. At Bosch, **250+ Python regression scenarios per cycle** maintained stability across 6 production releases.

At Qualcomm, I'd treat NPU platform software the same way — if the execution environment fails, every ML feature above it fails silently. That layer deserves the same rigor as automotive safety software.

---

### Q6: "Walk me through how you debug a hard embedded bug"

My process has four stages: observe, hypothesize, instrument, verify.

**Observe first.** Look for patterns before touching anything. When does it fail? Under what load? How often? At GM, the stack overflow only triggered during high-load CAN FD diagnostic sessions — that pattern immediately pointed to resource exhaustion, not a logic error.

**Hypothesize with ranking.** Form two or three specific, testable hypotheses ranked by likelihood. For the stack overflow: (1) stack overflow, (2) ISR re-entrancy, (3) pointer corruption from a CAN buffer. Start with the most testable one.

**Instrument without changing behavior.** Add observability that doesn't perturb the system: JTAG watchpoints, GPIO toggles + logic analyzer, firmware logging with timestamps, map-file inspection. The goal is to capture state at the moment of failure — not after. At Bosch, simultaneous traces on UART, SPI, and CAN correlated an interrupt storm to the latency spike in under an hour.

**Verify the fix, then add a tripwire.** Reproduce the original failure mode explicitly after the fix. Then add a permanent detection mechanism — an MPU guard, a watermark check, a power-interruption test — so the same class of bug can't silently regress. This is how I added power-cut emulation to our OTA test suite after an atomicity regression.

This process maps directly to debugging MMU faults, cache coherency issues, or IPC timeouts on Snapdragon — the tools change, the discipline doesn't.

---

### Q7: "Describe your experience with serial/bus protocols — CAN, SPI, UART"

**At GM:** CAN FD and UDS are my primary stack. I implemented communication for **15+ distributed nodes** — DBC message layout design, CAN frame parsers, UDS diagnostic session state machines with timeout and retry logic. My CAPL test nodes in Vector CANoe simulate all peer ECUs simultaneously, including fault injection. This let us run **180+ integration scenarios per build** and reduce **diagnostic session failures by 22 per release cycle**.

**At Bosch:** I configured **UART, SPI, and CAN** interfaces for GNSS receivers — clock stretching, framing, arbitration, and the timing constraints between the GNSS chipset and the host controller. I improved signal integrity across **120+ validation scenarios** and reduced debugging time by **18 hours per release** through better instrumentation and logging.

The analogy to Qualcomm's IPC is direct: designing bus protocols is the same engineering problem as designing shared-memory IPC. In both cases you define message formats, handle errors and retries, manage timing and buffer ownership, and debug with traces. The medium changes — from CAN to ring buffers and doorbell interrupts — but the discipline is identical.

---

### Q8: "How do you manage memory in constrained embedded systems?"

I treat memory as a first-class design constraint.

**Static placement via linker scripts:** I explicitly control where every section lands — code in flash, constants in .rodata, zero-initialized globals in .bss, initialized globals in .data. For stack sizing, I don't guess — I enable pattern fills at startup and measure watermarks under worst-case load. This discipline let me find and fix the stack overflow that reclaimed **48 KB** across four tasks at GM.

**DMA-safe buffers:** I keep DMA buffers in dedicated memory regions aligned to cache-line boundaries. Explicit cache clean before DMA reads from CPU-written buffers; explicit invalidate after DMA writes before CPU reads results. No assumptions about implicit coherency.

**No dynamic allocation in real-time paths:** For variable-size buffers, I use statically allocated pools. At GM, I designed **reusable HAL components** that standardized peripheral buffer management and reduced integration effort by **25 hours per release cycle** while improving portability across hardware platforms.

At the Qualcomm scale — managing on-chip NPU SRAM vs DRAM vs scratchpad — the same disciplines apply: explicit placement, lifetime analysis, alignment for DMA and cache, and profiling under real workloads with hardware performance counters.

---

### Q9: "Describe your testing and validation experience"

I've worked across three levels: component/unit, integration, and system/HIL.

**Integration (GM):** Vector CANoe with CAPL scripting. My harness simulates all 15+ peer ECUs and injects fault conditions — bus-off, missing messages, out-of-sequence frames, voltage glitches. **180+ integration scenarios per build, 35+ critical defects caught before system testing**.

**Component/unit (Bosch):** Python-based test cases on virtual validation (SIL) environments. **250+ regression scenarios per cycle** across **6 production releases** — catching regressions within hours of a commit and maintaining build stability.

**HIL:** Real hardware in automated test racks, validated under realistic power, temperature, and signal conditions for corner-case behavior.

**OTA-specific:** I added power-interruption emulation (relay-controlled supply cut during flash write) to the regression suite after an atomicity regression. This test caught two additional edge cases in subsequent builds before they hit fleet hardware — a lesson that clean power-cycle simulation is not sufficient for bootloader testing.

For Qualcomm, I'd apply the same approach: unit tests for NPU platform APIs, integration tests for CPU↔NPU command flows, and fault-injection tests for timeout and error-recovery paths.

---

### Q10: "Tell me about working across hardware, firmware, and systems teams"

Cross-functional collaboration has been constant in both roles. The most challenging incident at GM was a memory map conflict discovered during integration — the SoC vendor's bring-up firmware used different peripheral base addresses than our hardware spec. The hardware team had already taped out the PCB.

Rather than escalating as a blocker, I documented the conflict precisely: mapped the overlapping address ranges, identified exactly which driver modules (DMA, CAN, NVM) were affected and under what traffic conditions, and quantified the risk. I set up a joint review with the hardware integration lead, the systems engineer, and the vendor's FAE, and presented two resolution options with timelines and risk assessments.

The vendor confirmed it was a silicon rev B issue they hadn't communicated. I negotiated accelerated rev B sample delivery while in parallel adding a runtime silicon-revision validation check to the startup code. Integration testing started on schedule; the runtime check caught an accidental rev A board in testing and prevented a misleading bug report.

The lesson I bring: cross-team work moves forward when you show up with a specific, quantified impact analysis — not just a bug report. I'd apply the same approach at Qualcomm coordinating between NPU hardware, DSP firmware, and platform software teams.

---

### Q11: "What's your bootloader and firmware update experience?"

At GM, I own the bootloader and OTA update mechanism for production ECUs on ARM Cortex-M. This includes:

- Minimal **startup code** that validates reset cause before jumping to application or bootloader.
- **Flash driver** with sector erase, write verification, and MISRA-compliant error handling.
- **Secure flashing** — SHA-based hash verification of firmware images before execution, with rollback-safe flag writes using multi-byte atomic operations.
- **Watchdog-safe timing** throughout the update sequence — the watchdog must be fed at each stage or the ECU resets to known-good firmware.
- **UDS integration** — OTA updates triggered over CAN FD using UDS routines, with progress reporting and error codes.

Result: **zero rollback failures across 9 consecutive software releases**.

At Bosch, I integrated and verified GNSS firmware updates in **Python-based virtual validation environments**, running **250+ regression scenarios per cycle** across **6 production releases**.

At Qualcomm, the same mindset applies to NPU secure boot, firmware image authentication, and field-update mechanisms for accelerator firmware — the consequences of getting atomicity wrong are identical.

---

### Q12: "Why move from automotive to Qualcomm / mobile SoC?"

It's less a transition and more a natural scaling up. The engineering problems I've been solving in automotive — real-time multi-node IPC, cache-coherent shared memory, interrupt-driven data pipelines, memory-constrained firmware, safety-critical boot sequences — are the same problems at the core of Qualcomm's NPU platform. The medium shifts from CAN networks to on-chip interconnects, and the performance targets tighten from milliseconds to microseconds, but the skills are directly transferable.

What excites me about Qualcomm is the NPU and DSP layer. On-device AI inference is where embedded software is heading, and working on the execution substrate — the runtime that partitions and schedules workloads across CPU, DSP, and NPU — is exactly the kind of system-level challenge I want. My AUTOSAR background (layered software components, defined execution environments, strict interface contracts) is architecturally similar to how Qualcomm structures platform software for heterogeneous compute.

Automotive embedded gave me discipline: safety standards, formal requirements, systematic testing under production constraints. Qualcomm gives me scale and the chance to work on silicon that ships in hundreds of millions of devices. That's a compelling combination and the right next step.

---

## Coding Answer 1 – Reverse a Singly Linked List

**Thought process:** In embedded C, reversing a singly linked list in place requires careful pointer manipulation without extra memory. I maintain three pointers: `prev`, `curr`, and `next`. Starting from the head, I iteratively redirect each node's `next` pointer to point backward to `prev`, advancing all three pointers until the end. At the end of the loop, `prev` holds the new head. This pattern is safe for memory-constrained systems because it does not allocate additional nodes and only uses a constant number of temporary variables. It also matches how we think about in-place transformations in ECU data structures, where predictability and minimal allocation are important.

**Time:** O(n) | **Space:** O(1)

```c
struct Node {
    int data;
    struct Node *next;
};

struct Node* reverse_list(struct Node *head) {
    struct Node *prev = NULL;
    struct Node *curr = head;
    struct Node *next = NULL;

    while (curr != NULL) {
        next = curr->next;   // save next node
        curr->next = prev;   // reverse the link
        prev = curr;         // advance prev
        curr = next;         // advance curr
    }

    return prev;             // prev is now the new head
}
```


## Coding Answer 2 – Detect Loop in a Singly Linked List

**Thought process:** To detect a loop in a singly linked list efficiently, I use the **Floyd cycle detection** algorithm (tortoise-and-hare). Two pointers, `slow` and `fast`, both start at the head. On each iteration, `slow` moves one node while `fast` moves two nodes. If there is no loop, `fast` reaches `NULL`. If a loop exists, `slow` and `fast` will meet inside the cycle. This approach runs in linear time with constant extra memory and does not modify the list structure, which is important if other modules rely on the list's integrity.

**Time:** O(n) | **Space:** O(1)

```c
int has_loop(struct Node *head) {
    struct Node *slow = head;
    struct Node *fast = head;

    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;

        if (slow == fast) {
            return 1;   // loop detected
        }
    }

    return 0;           // no loop
}
```


## Coding Answer 3 – Implement strstr (Find Substring) in C

**Thought process:** Implementing `strstr` in plain C tests pointer arithmetic and edge cases. I take two strings: `haystack` and `needle`. If `needle` is empty, I return `haystack` per standard behavior. Otherwise, I iterate over each possible starting position in `haystack` and compare characters against `needle` one by one. If all characters match, I return a pointer to the start of the occurrence; if the end of `haystack` is reached without a full match, I return `NULL`. This is an O(n × m) solution, acceptable in embedded environments where strings are not extremely large. In automotive firmware, this pattern appears when scanning diagnostic identifiers stored in flash. I would mention KMP for better worst-case complexity but implement the clear version first.

**Time:** O(n × m) | **Space:** O(1)

```c
#include <stddef.h>

char* my_strstr(const char *haystack, const char *needle) {
    if (*needle == '\0') {
        return (char *)haystack;     // empty needle: return haystack
    }

    for (const char *h = haystack; *h != '\0'; h++) {
        const char *p = h;
        const char *q = needle;

        while (*p != '\0' && *q != '\0' && *p == *q) {
            p++;
            q++;
        }

        if (*q == '\0') {
            return (char *)h;        // full match found
        }

        if (*p == '\0') {
            break;                   // haystack exhausted
        }
    }

    return NULL;
}
```


## Coding Answer 4 – Safe memcpy with Overlap Handling (Like memmove)

**Thought process:** A classic low-level question is to implement a `memcpy`-like function that correctly handles overlapping regions. In embedded systems, getting this wrong can corrupt critical buffers. If the destination starts after the source and overlaps, we copy bytes from the end backwards; otherwise, we copy forwards from the beginning. This ensures bytes are not overwritten before being read. I use `unsigned char` pointers for byte-wise access. In production code, we might add alignment-based word-copy optimizations, but the essential logic is direction selection based on pointer comparison. This is directly relevant to Qualcomm-style platform software where shared buffers are moved between CPU, DSP, and NPU.

**Time:** O(n) | **Space:** O(1)

```c
#include <stddef.h>

void* my_memmove(void *dest, const void *src, size_t n) {
    unsigned char *d = (unsigned char *)dest;
    const unsigned char *s = (const unsigned char *)src;

    if (d == s || n == 0) {
        return dest;
    }

    if (d < s || d >= s + n) {
        // no harmful overlap — copy forward
        for (size_t i = 0; i < n; i++) {
            d[i] = s[i];
        }
    } else {
        // overlapping with dest after src — copy backward
        for (size_t i = n; i > 0; i--) {
            d[i - 1] = s[i - 1];
        }
    }

    return dest;
}
```


## Coding Answer 5 – Count Pairs with Sum Divisible by k

**Thought process:** Given an array of integers and an integer `k`, count pairs whose sum is divisible by `k`. An efficient approach uses a frequency array of size `k` counting how many numbers have each remainder when divided by `k`. Pairs with remainder `r` and `k − r` form valid pairs. Remainder 0 pairs with itself, and when `k` is even the middle remainder (`k/2`) also pairs with itself. The algorithm is O(n + k) time and O(k) space, which is predictable and small when `k` is modest. I pay attention to negative remainders, integer overflow, and the even-k edge case.

**Time:** O(n + k) | **Space:** O(k)

```c
#include <stddef.h>

long long count_pairs_divisible_by_k(const int *arr, size_t n, int k) {
    long long count = 0;
    int freq[1024] = {0};   // assumes k <= 1024

    for (size_t i = 0; i < n; i++) {
        int rem = arr[i] % k;
        if (rem < 0) {
            rem += k;        // normalize negative remainder
        }
        freq[rem]++;
    }

    // remainder 0: any two elements with rem 0 form a valid pair
    count += (long long)freq[0] * (freq[0] - 1) / 2;

    // symmetric pairs: rem r pairs with rem k-r
    for (int r = 1; r < k - r; r++) {
        count += (long long)freq[r] * freq[k - r];
    }

    // middle remainder (only when k is even): pairs among themselves
    if (k % 2 == 0) {
        int mid = k / 2;
        count += (long long)freq[mid] * (freq[mid] - 1) / 2;
    }

    return count;
}
```

---

## 6. Additional Coding Problems with Answers

### 6.1 – Find Length of Loop in a Linked List

**Thought process:** First detect the loop using Floyd's algorithm. Once `slow == fast` inside the cycle, keep `slow` fixed and walk `fast` one step at a time, counting until `fast` returns to `slow`. This gives the exact loop length without modifying the list.

**Time:** O(n) | **Space:** O(1)

```c
int loop_length(struct Node *head) {
    struct Node *slow = head, *fast = head;

    while (fast != NULL && fast->next != NULL) {
        slow = slow->next;
        fast = fast->next->next;

        if (slow == fast) {
            // loop confirmed — count nodes in cycle
            int len = 1;
            struct Node *curr = slow->next;
            while (curr != slow) {
                curr = curr->next;
                len++;
            }
            return len;
        }
    }

    return 0;   // no loop
}
```


### 6.2 – Intersection Point of Two Singly Linked Lists

**Thought process:** Compute the lengths of both lists. Advance a pointer on the longer list by the length difference so both pointers are equidistant from the tail. Then advance both one step at a time; the first node where they are equal is the intersection. This avoids any extra memory allocation. Important: if they do not intersect, both pointers reach `NULL` simultaneously and we return `NULL`.

**Time:** O(n + m) | **Space:** O(1)

```c
struct Node* find_intersection(struct Node *headA, struct Node *headB) {
    if (!headA || !headB) return NULL;

    int lenA = 0, lenB = 0;
    struct Node *a = headA, *b = headB;

    while (a) { lenA++; a = a->next; }
    while (b) { lenB++; b = b->next; }

    a = headA;
    b = headB;

    // advance the longer list
    while (lenA > lenB) { a = a->next; lenA--; }
    while (lenB > lenA) { b = b->next; lenB--; }

    // move both until they meet
    while (a != b) {
        a = a->next;
        b = b->next;
    }

    return a;   // NULL if no intersection
}
```


### 6.3 – Convert Sorted Linked List to BST

**Thought process:** Use the slow/fast pointer pattern to find the midpoint of the list. The midpoint becomes the root. Recurse on the left half (head to one node before mid) and the right half (mid->next to tail). I pass a `tail` sentinel pointer to delimit the sublist boundaries, avoiding any O(n) re-scan each time. This gives a height-balanced BST because we always pick the middle as root.

**Time:** O(n log n) | **Space:** O(log n) stack

```c
#include <stdlib.h>

struct TreeNode {
    int val;
    struct TreeNode *left, *right;
};

static struct Node* find_mid(struct Node *head, struct Node *tail) {
    struct Node *slow = head, *fast = head;
    while (fast != tail && fast->next != tail) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}

struct TreeNode* sorted_list_to_bst(struct Node *head, struct Node *tail) {
    if (head == tail) return NULL;

    struct Node *mid = find_mid(head, tail);

    struct TreeNode *root = (struct TreeNode *)malloc(sizeof(struct TreeNode));
    root->val = mid->data;
    root->left  = sorted_list_to_bst(head, mid);
    root->right = sorted_list_to_bst(mid->next, tail);
    return root;
}
```

Call with: `sorted_list_to_bst(head, NULL)`.


### 6.4 – Reverse Bits of a 32-bit Integer

**Thought process:** For each of the 32 bit positions, extract the LSB of `n`, shift it into the correct position of `result`, then shift `n` right. This is the straightforward O(32) approach. In embedded C this is the clearest and most portable version. An alternative is a lookup-table on nibbles for speed-critical paths.

**Time:** O(1) — fixed 32 iterations | **Space:** O(1)

```c
#include <stdint.h>

uint32_t reverse_bits(uint32_t n) {
    uint32_t result = 0;

    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1u);   // shift result left, bring in LSB of n
        n >>= 1;
    }

    return result;
}
```


### 6.5 – Count Set Bits (Brian Kernighan's Algorithm)

**Thought process:** `n & (n - 1)` clears the lowest set bit of `n`. Repeatedly applying this and counting iterations gives the number of set bits. This runs in O(k) where k is the number of set bits, which is faster than scanning all 32 bits when the number is sparse. Embedded register status checks often have sparse bits, making this the preferred approach.

**Time:** O(k) where k = number of set bits | **Space:** O(1)

```c
int count_set_bits(unsigned int n) {
    int count = 0;

    while (n) {
        n &= (n - 1);   // clear lowest set bit
        count++;
    }

    return count;
}
```


### 6.6 – Check if a Number is a Power of Two

**Thought process:** A power of two has exactly one set bit. Therefore `n & (n - 1)` equals zero for powers of two (clears the single set bit, leaving nothing). We also guard against `n <= 0` because the formula would wrongly return true for zero. This single-expression check is a standard embedded interview pattern for flag and mask validation.

**Time:** O(1) | **Space:** O(1)

```c
int is_power_of_two(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}
```


### 6.7 – Reverse a String in C (In-Place, No Library)

**Thought process:** Use two pointers starting at the beginning and the end of the string. Swap characters and move inward until they cross. I find the end without `strlen` by walking a pointer to the null terminator, which avoids a second pass. This is the standard embedded approach: no dynamic allocation, no library calls, fixed and predictable execution time.

**Time:** O(n) | **Space:** O(1)

```c
void reverse_string(char *str) {
    if (!str || !*str) return;

    char *end = str;
    while (*end) end++;   // walk to null terminator
    end--;                // step back to last character

    while (str < end) {
        char tmp = *str;
        *str++ = *end;
        *end-- = tmp;
    }
}
```


### 6.8 – Check If One Array Is a Subset of Another

**Thought process:** For each element of the candidate subset, search the main array. The simple O(n × m) nested loop is correct and predictable in memory, which matters in embedded contexts where hash maps may not be available. If the arrays are sorted, we can do this in O(n + m) with two pointers. I always mention the trade-off — sorting costs O(n log n) upfront but amortizes across many subset checks.

**Time:** O(n × m) naive; O(n log n + m) with sorting | **Space:** O(1)

```c
int is_subset(const int *arr, size_t n, const int *sub, size_t m) {
    for (size_t i = 0; i < m; i++) {
        int found = 0;
        for (size_t j = 0; j < n; j++) {
            if (sub[i] == arr[j]) {
                found = 1;
                break;
            }
        }
        if (!found) return 0;
    }
    return 1;
}
```


### 6.9 – Rotate Array by k Positions

**Thought process:** The three-reversal trick rotates an array in O(n) time with O(1) extra space. For a right rotation by `k`: reverse the first `n-k` elements, reverse the last `k` elements, then reverse the entire array. Modulo `k` by `n` first to handle cases where `k >= n`. This avoids shifting elements one by one k times (which would be O(n × k)).

**Time:** O(n) | **Space:** O(1)

```c
static void reverse_range(int *arr, int left, int right) {
    while (left < right) {
        int tmp = arr[left];
        arr[left++] = arr[right];
        arr[right--] = tmp;
    }
}

void rotate_right(int *arr, int n, int k) {
    if (n == 0) return;
    k = k % n;
    if (k == 0) return;

    reverse_range(arr, 0, n - k - 1);   // reverse first part
    reverse_range(arr, n - k, n - 1);   // reverse second part
    reverse_range(arr, 0, n - 1);       // reverse whole array
}
```


### 6.10 – Find Missing Number in 1..n

**Thought process:** XOR all values from 1 to n, then XOR all elements in the array. Every number that appears in both cancels out (x ^ x = 0), leaving only the missing number. This is O(n) time with O(1) space and avoids overflow issues that a sum-based approach can hit for large n. It works because XOR is commutative and associative.

**Time:** O(n) | **Space:** O(1)

```c
int find_missing(const int *arr, int n) {
    int xor_all = 0;
    int xor_arr = 0;

    for (int i = 1; i <= n; i++) {
        xor_all ^= i;
    }
    for (int i = 0; i < n - 1; i++) {
        xor_arr ^= arr[i];
    }

    return xor_all ^ xor_arr;   // the missing number
}
```


### 6.11 – Check If a Binary Tree Is a BST

**Thought process:** Naively checking `left->val < root->val < right->val` at each node fails for deep trees because it ignores the global min/max bounds. The correct approach threads a valid range `(min, max)` through the recursion. At each node, we verify the value is strictly within bounds, then recurse with a tighter bound. Starting with `(INT_MIN, INT_MAX)` lets us catch any violation anywhere in the tree.

**Time:** O(n) | **Space:** O(h) stack, h = tree height

```c
#include <limits.h>

struct TreeNode {
    int val;
    struct TreeNode *left, *right;
};

static int is_bst_helper(struct TreeNode *node, int min_val, int max_val) {
    if (!node) return 1;
    if (node->val <= min_val || node->val >= max_val) return 0;

    return is_bst_helper(node->left,  min_val, node->val) &&
           is_bst_helper(node->right, node->val, max_val);
}

int is_bst(struct TreeNode *root) {
    return is_bst_helper(root, INT_MIN, INT_MAX);
}
```


### 6.12 – Left View of a Binary Tree

**Thought process:** The left view is the first node visible at each level when the tree is viewed from the left. A BFS (level-order traversal) using a queue naturally groups nodes by level. For each level, print the first node encountered. I use a fixed-size array as a queue since dynamic allocation is avoided in embedded environments. The level_size variable tracks how many nodes belong to the current level.

**Time:** O(n) | **Space:** O(w), w = max width of tree

```c
#include <stdio.h>

void left_view(struct TreeNode *root) {
    if (!root) return;

    struct TreeNode *queue[4096];
    int front = 0, rear = 0;
    queue[rear++] = root;

    while (front < rear) {
        int level_size = rear - front;

        for (int i = 0; i < level_size; i++) {
            struct TreeNode *node = queue[front++];

            if (i == 0) {
                printf("%d ", node->val);   // first node at this level
            }
            if (node->left)  queue[rear++] = node->left;
            if (node->right) queue[rear++] = node->right;
        }
    }
}
```

---

## 7. Embedded C Keyword & Concept Q&A

These are frequently asked in Qualcomm verbal/whiteboard rounds. Practice stating these in 2–3 sentences.

---

**Q: What is `volatile` and when do you use it?**

`volatile` tells the compiler that a variable's value can change at any time outside the program's normal control flow — by an ISR, another core, or a hardware register. Without it, the compiler may cache the value in a register and never re-read memory, causing bugs in polling loops and shared flags.

Use cases:
- Hardware status/control registers mapped to fixed addresses (MMIO).
- Variables read in a main loop but written in an ISR.
- Spin-wait loops waiting for a flag set by another thread or hardware.

```c
volatile uint32_t *UART_STATUS = (volatile uint32_t *)0x40001000;
volatile int data_ready = 0;   // set by ISR, polled by main loop
```

---

**Q: What is `const` and how is it different from `#define`?**

`const` creates a typed, scoped, debugger-visible constant. The compiler enforces type checking and the constant has an address. `#define` is a preprocessor text substitution with no type, no scope, and no address.

Prefer `const` in embedded code because:
- Debuggers can inspect the value by name.
- The compiler can place it in `.rodata` / flash automatically.
- Type mismatches are caught at compile time.

```c
#define MAX_RETRIES 5          // no type, no scope, no debug visibility
const int max_retries = 5;     // typed, scoped, in .rodata
```

---

**Q: What are the two uses of `static` in C?**

1. **Inside a function:** Makes a local variable persist across function calls (stored in `.bss`/`.data` instead of stack). Useful for state machines and counters in ISRs.
2. **At file scope:** Restricts the symbol's linkage to the current translation unit, preventing name collisions across files.

```c
void tick_counter(void) {
    static uint32_t count = 0;   // survives between calls
    count++;
}

static void helper(void) { }    // not visible outside this .c file
```

---

**Q: What does `extern` do?**

`extern` declares that a variable or function is defined in another translation unit. It tells the compiler the symbol exists without emitting storage for it. The linker resolves the reference at link time.

```c
// file_a.c
int g_shared = 0;

// file_b.c
extern int g_shared;   // declaration only; storage is in file_a.c
```

Common mistake: `extern int x = 5;` is both a declaration and a definition — redundant and potentially confusing.

---

**Q: What is `restrict` and when does it matter?**

`restrict` is a promise to the compiler that the pointed-to memory is not aliased by any other pointer in the current scope. This allows the compiler to generate better vectorized or load/store-reordered code because it doesn't need to re-read memory after each store.

```c
void optimized_copy(int *restrict dst, const int *restrict src, size_t n) {
    for (size_t i = 0; i < n; i++) dst[i] = src[i];
}
```

Lying about aliasing (i.e., using `restrict` on overlapping buffers) is undefined behavior. It is particularly useful for DSP-style loops on Hexagon or ARM NEON.

---

**Q: When do you use `inline`?**

`inline` is a hint (not a command) for the compiler to expand the function body at the call site, eliminating function call overhead. Useful for very small, frequently called functions — register accessors, bit-manipulation utilities — where the call overhead would dominate.

Caveats in embedded:
- Aggressive inlining increases code size; flash is limited.
- `static inline` in a header is the standard way to expose inlinable utilities across translation units.
- MISRA C discourages macro-based inlining; prefer `static inline` functions.

---

**Q: What does `__attribute__((packed))` do and what are the risks?**

It instructs the compiler to suppress padding between struct members, so the struct occupies the minimum possible bytes. Used when mapping structs directly onto network/serial protocol frames or hardware register layouts.

Risk: Accessing unaligned members of a packed struct on ARM can generate a data abort or a slow unaligned access exception. Always access packed members with `memcpy` when unsure of alignment.

```c
typedef struct __attribute__((packed)) {
    uint8_t  cmd;
    uint16_t payload_len;   // sits at byte offset 1 — unaligned on ARM
    uint32_t checksum;
} msg_header_t;
```

---

**Q: What does `volatile const` mean?**

It means the variable is read-only from the software's perspective (`const`) but can still change at any time due to hardware (`volatile`). The canonical use case is a hardware status register that the CPU must always read fresh from memory but must never write to.

```c
volatile const uint32_t *CHIP_ID = (volatile const uint32_t *)0x50000000;
```

---

## 8. OS / RTOS / Concurrency Verbal Q&A

---

**Q: What is priority inversion and how does priority inheritance fix it?**

**Priority inversion** occurs when a high-priority task is blocked waiting for a resource held by a low-priority task, and a medium-priority task preempts the low-priority task, preventing it from releasing the resource. The high-priority task is effectively stuck behind the medium-priority one despite having higher priority.

**Priority inheritance** is the fix: when a low-priority task holds a mutex that a high-priority task needs, the OS temporarily elevates the low-priority task's priority to match the waiting task. This prevents medium-priority tasks from preempting it, allowing it to finish quickly and release the mutex.

Real-world example: Mars Pathfinder experienced a priority inversion in 1997 due to a VxWorks mutex without priority inheritance enabled.

---

**Q: What is the difference between a mutex and a binary semaphore?**

| Property | Mutex | Binary Semaphore |
|---|---|---|
| Ownership | Yes — only the locker can unlock | No — any task can signal |
| Priority inheritance | Typically supported | Typically not |
| Use case | Mutual exclusion of a shared resource | Signaling between tasks |
| Death handling | Some RTOSes detect mutex holder death | N/A |

Key rule: **Use a mutex for protecting shared data; use a binary semaphore for task synchronization/signaling.** Unlocking a mutex you don't own is undefined behavior in most RTOSes.

---

**Q: When do you use a counting semaphore?**

A counting semaphore tracks a pool of N identical resources. The classic use case is a bounded producer-consumer buffer: the semaphore is initialized to N (empty slots). Producers `wait` before filling a slot (blocks when full); consumers `signal` after consuming (increments the count). A second semaphore initialized to 0 tracks filled slots for the consumer side.

Also used for: connection pool limits, rate limiting, signaling that N events have occurred.

---

**Q: What are the four Coffman conditions for deadlock?**

All four must hold simultaneously for a deadlock to occur. Removing any one prevents deadlock.

1. **Mutual exclusion** — At least one resource is held in a non-shareable mode.
2. **Hold and wait** — A task holds at least one resource while waiting to acquire more.
3. **No preemption** — Resources cannot be forcibly taken from a task.
4. **Circular wait** — A set of tasks each waits for a resource held by the next in the set.

Prevention strategies: order resource acquisition consistently to break circular wait; use try-lock with timeout to break hold-and-wait.

---

**Q: How do you write a correct ISR?**

Rules for an ISR in embedded / RTOS environments:

1. **Keep it short.** Do the minimum necessary — read the status register, copy data to a buffer, set a flag.
2. **No blocking calls.** Never call `mutex_lock`, `sleep`, or any function that can block.
3. **No dynamic allocation.** `malloc`/`free` are not re-entrant or interrupt-safe.
4. **Use `volatile` flags** for variables shared with the main loop or tasks.
5. **Defer heavy work.** Post to a queue, set a semaphore, or use a software interrupt to wake a handler task.
6. **Acknowledge the interrupt.** Clear the hardware interrupt pending bit before exiting to avoid immediate re-entry.

```c
volatile int uart_rx_flag = 0;
char uart_rx_buf[64];

void UART_IRQHandler(void) {
    uart_rx_buf[0] = UART->DATA;   // read received byte
    uart_rx_flag = 1;              // signal main loop
    UART->STATUS = UART_STATUS_RX; // clear interrupt pending bit
}
```

---

**Q: What is the difference between top-half and bottom-half interrupt handling?**

- **Top-half (hardirq):** The actual interrupt handler that runs at interrupt priority. Must be extremely fast. Only does time-critical work: reading hardware state, clearing the interrupt, saving raw data.
- **Bottom-half:** Deferred work scheduled by the top-half to run in a less privileged context. Examples in Linux: softirqs, tasklets, workqueues. In an RTOS: a handler task woken by a semaphore from the ISR.

The split ensures the system remains responsive to other interrupts while heavy processing (DMA completion handling, protocol parsing, buffer management) happens safely in thread context.

---

**Q: What happens during a context switch on ARM Cortex-M?**

When the RTOS scheduler decides to switch tasks:

1. The processor (or RTOS's PendSV handler) saves the running task's context: core registers R0–R12, LR, PC, PSR are pushed onto the current task's stack by the hardware automatically on exception entry.
2. RTOS saves additional registers (R4–R11) that the hardware does not save automatically.
3. The stack pointer (PSP) for the current task is saved in the TCB (Task Control Block).
4. The scheduler selects the next task and loads its PSP.
5. The saved registers for the new task are restored from its stack.
6. Exception return restores PC and PSR, resuming the new task at the point it was suspended.

On Cortex-M, the PendSV exception is used for context switches because it has the lowest configurable priority and can be safely preempted by all other exceptions.

---

**Q: When should you use a spinlock vs a mutex?**

- **Spinlock:** Burns CPU in a tight loop until the lock is free. Zero overhead when contention is rare and the critical section is very short (a few instructions). **Only safe in non-preemptible context or when the holder cannot sleep** — e.g., kernel interrupt context, bare-metal ISRs.
- **Mutex:** Puts the waiting task to sleep (blocked state), saving CPU. Adds scheduling overhead (context switch cost). Correct choice for user-space / RTOS tasks where the critical section may be tens of microseconds or longer.

Rule of thumb: if the critical section is shorter than the context switch overhead (typically 1–5 µs on Cortex-M), a spinlock may be faster. Otherwise, use a mutex.

---

**Q: How do you detect and prevent stack overflow?**

Detection methods:
1. **Stack canary / pattern fill:** Fill the stack with a known value (e.g., `0xDEADBEEF`) at init. Periodically check if the pattern near the stack limit has been overwritten.
2. **MPU stack guard:** Configure the ARM Memory Protection Unit to mark the last page of each task stack as no-access. An overflow triggers a MemManage fault.
3. **High-watermark tracking:** At runtime, walk the stack from the limit upward to find where the fill pattern ends; report the maximum usage.

Prevention:
- Avoid large local arrays on stack; allocate them statically or in heap pools.
- Avoid deep recursion; convert to iterative with an explicit stack.
- Review linker map files for stack size estimates and add safety margins.

---

## 9. IPC / SoC System Design Q&A

---

### 9.1 – Design a CPU→NPU Command Queue

**Question:** How would you design a command submission and completion interface between the CPU and an NPU that cannot share the CPU's cache?

**Design:**

Use a **ring buffer in non-cached shared memory** accessible by both CPU and NPU via their respective memory maps.

```
CPU (ARM Application Core)            NPU (Accelerator Core)
 ┌──────────────────────┐             ┌──────────────────────┐
 │  1. Fill descriptor  │             │  5. Read descriptor  │
 │  2. Cache clean      │             │  6. Execute workload │
 │  3. Write WRITE_IDX  │─── MMIO ──▶│  7. Write READ_IDX   │
 │  4. Ring doorbell    │◀── IRQ ────│  8. Assert completion │
 └──────────────────────┘             └──────────────────────┘
            │                                     │
            └──────────── Shared SRAM ────────────┘
                  [desc0][desc1][desc2][desc3]
                   write_idx         read_idx
```

**Key components:**

1. **Descriptor struct** — Contains input/output buffer addresses (physical), sizes, workload type, and a sequence number.
2. **Ring buffer** — Fixed-size array of descriptors in non-cached shared SRAM. `write_idx` advanced by CPU; `read_idx` advanced by NPU.
3. **Cache maintenance** — Before the CPU writes `write_idx`, it must `DC CVAC` (clean to PoC) the descriptor so the NPU sees it. After NPU writes results, CPU must `DC CIVAC` (invalidate) result buffers before reading.
4. **Doorbell interrupt** — CPU writes to an MMIO register to notify NPU of new work. NPU signals CPU via a completion IRQ on finish.
5. **Error handling** — Descriptor has a status field. CPU polls or IRQ-notifies. Timeout watchdog fires if NPU does not complete within a deadline; CPU resets the NPU subsystem.

**Capacity planning:** Size the ring so peak burst of commands can queue without back-pressure dropping frames. Use `(write_idx - read_idx) % N` for occupancy check.

---

### 9.2 – Shared Memory Between Two Non-Coherent Asymmetric Cores

**Question:** CPU and DSP share a buffer in DRAM, but the interconnect is non-cache-coherent. How do you ensure data integrity?

**Protocol:**

```
CPU side                          DSP side
────────                          ────────
1. Write data to buffer
2. DC CVAC (clean cache lines)
3. DSB SY (wait for clean)
4. Write OWNER = DSP in handshake reg
5. Ring doorbell ─────────────────────▶ 6. Read OWNER; confirm == DSP
                                        7. DC CIVAC (invalidate cache lines)
                                        8. DSB SY
                                        9. Read and process buffer
                                       10. Write results
                                       11. DC CVAC (clean results)
                                       12. DSB SY
                                       13. Write OWNER = CPU
                                       14. Assert completion IRQ ◀────────
15. DC CIVAC result lines
16. DSB SY
17. Read results
```

**Rules:**
- The ownership handshake register must be in non-cached memory or both sides must use the same cache-coherent path.
- `DSB SY` ensures all prior memory operations are visible before the flag write.
- Never access a buffer without first confirming ownership via the handshake — avoids the race where one core reads while the other is still writing.

---

### 9.3 – Designing a DMA Transfer

**Question:** Walk me through setting up a DMA transfer from a peripheral to DRAM on an embedded SoC.

**Steps:**

1. **Allocate aligned buffer** — DMA controllers typically require 4-byte or cache-line-aligned (64-byte) buffers. Use a static or pool allocator.
2. **Invalidate destination cache** — Before the DMA starts, `DC CIVAC` the destination buffer so stale CPU cache lines do not overwrite DMA results when evicted later.
3. **Configure DMA descriptor** — Source address (peripheral FIFO), destination address (DRAM buffer), transfer size, burst size, peripheral request signal.
4. **Enable DMA channel** — Start the transfer.
5. **Wait for completion** — Via DMA completion IRQ or polling the DMA status register (prefer IRQ).
6. **DSB after completion** — Ensure DMA writes are globally visible before CPU reads the buffer.
7. **Read buffer** — CPU reads the now-fresh data.

**Source buffer (CPU → peripheral):**
1. Write data to buffer.
2. `DC CVAC` + `DSB SY` to push data to DRAM before DMA reads it.
3. Configure and start DMA.

Common bug: invalidating the destination *after* DMA starts — a CPU cache eviction during the transfer can corrupt DMA results.

---

### 9.4 – Latency vs Throughput in NPU Workload Batching

**Question:** When should you batch NPU commands vs submit them individually?

**Trade-off table:**

| Strategy | Latency | Throughput | Power | When to use |
|---|---|---|---|---|
| Submit 1 command | Lowest (no wait) | Low (NPU underutilized) | Higher (frequent wake-up) | Interactive, real-time inference |
| Batch N commands | Higher (accumulate wait) | High (NPU fully pipelined) | Lower (fewer wake/sleep cycles) | Offline processing, camera pipeline |

**How to tune:**

- Use a **deadline-based flush**: accumulate commands up to N or until a timer fires (e.g., one display frame = 16 ms), whichever comes first. This bounds worst-case latency while still capturing batch efficiency.
- Profile NPU utilization with hardware performance counters. If utilization is < 60%, increase batch size. If p95 latency exceeds SLA, decrease it.
- For mixed workloads (real-time + background), maintain two separate queues with different priority levels and flush policies.

---

## 10. Behavioral STAR Stories (Vaishnavi Mysore)

### Story 1 – Debugging a Stack Overflow (Tough Debugging)

**Situation:** At General Motors, the ECU running a multi-task RTOS on ARM Cortex-M4 was intermittently resetting during extended diagnostic sessions over CAN FD, roughly once every four hours of testing. There were no fault codes logged and the reset counter incremented without any software exception being captured.

**Task:** I was responsible for root-causing and eliminating the reset before our next validation cycle, which was two weeks away.

**Action:**
1. Suspected stack overflow first because the reset pattern correlated with high-load diagnostic scenarios. Reviewed the linker map file — stack sizes were set by convention, not measured.
2. Enabled stack pattern fill (0xDEADBEEF) for all tasks in the startup code. On next reset, JTAG post-mortem inspection showed the pattern was completely overwritten near the diagnostic task's stack limit.
3. Used the JTAG debugger to set a watchpoint on the stack guard region. Reproduced the condition in 45 minutes and captured the exact call stack at the moment of overflow.
4. Found the root cause: the diagnostic state machine allocated a 2 KB temporary buffer as a local variable inside a deeply nested call chain. Combined with recursive CAN frame parsing, worst-case stack depth hit 6 KB against a 4 KB allocation.
5. Moved the buffer to `.bss` (static), flattened the recursion, and added an MPU guard page as a permanent tripwire.

**Result:** Zero resets across 200+ hours of subsequent validation. Recovered ~48 KB of usable stack headroom by removing oversized locals across four tasks. Delivered the fix two days before the validation cycle with a detailed root cause report reviewed by the hardware and systems teams.

---

### Story 2 – Performance Optimization Under Latency Constraints (Bosch GNSS)

**Situation:** At Robert Bosch, the GNSS processing firmware was experiencing periodic 80–120 ms latency spikes in position fix output. The system specification required fixes to be delivered within 20 ms of the measurement epoch. Spikes were causing downstream navigation errors in the vehicle path planner.

**Task:** Identify and eliminate the root cause of the latency spikes without increasing power consumption or refactoring the architecture.

**Action:**
1. Instrumented the firmware with microsecond-resolution GPIO toggles at each pipeline stage and captured traces with a logic analyzer.
2. Correlated spikes with a specific SPI peripheral ISR — a burst of 50–80 interrupts in under 1 ms from a noisy signal path was consuming 70% of CPU time, starving the GNSS processing task.
3. Added a debounce filter in hardware (RC filter recommendation to HW team) and changed the ISR to use edge-triggered rather than level-triggered detection, reducing interrupt storm to 2–3 events per event.
4. Moved the remaining SPI data reassembly from ISR top-half to a background task woken by a semaphore, keeping ISR execution under 5 µs.
5. Adjusted task priorities so the GNSS processing task preempted the SPI handler task when a new measurement epoch was pending.

**Result:** Average sensor latency improved by **12 ms**, worst-case spikes dropped from 120 ms to under 15 ms. Power consumption was unchanged. The fix was validated across temperature and noise corners in the HIL setup. Debugging time for future ISR-related issues was reduced by **18 hours per release cycle** through the improved instrumentation and logging hooks I added during the investigation.

---

### Story 3 – Cross-Team Conflict Resolution (HW/SW Memory Map)

**Situation:** During the integration phase of a new body control module at General Motors, I discovered that the memory map defined in the hardware specification did not match what the SoC vendor's bring-up firmware was using. Two peripheral base addresses conflicted, which would have caused the DMA controller to overwrite CAN FD receive buffers during high-traffic conditions. The hardware team had already taped out the PCB.

**Task:** Resolve the conflict between the HW spec, the silicon vendor's recommendation, and our existing firmware — with only three weeks before start of integration testing.

**Action:**
1. Documented the conflict precisely: mapped the overlapping address ranges, identified which firmware modules would be affected (DMA driver, CAN driver, NVM driver), and quantified the risk (data corruption under certain traffic patterns, not always triggered).
2. Set up a joint review with the hardware integration lead, the silicon vendor's FAE, and the test engineer. Presented a one-page impact analysis with two resolution options: remap in software vs. request a revised memory map from the vendor.
3. Vendor confirmed that two registers were remapped in a rev B silicon update they had not communicated. We were still on rev A samples.
4. Negotiated an accelerated sample delivery of rev B parts for firmware bring-up. In parallel, I added a runtime address validation check in the firmware startup that would assert if the wrong silicon revision was detected.

**Result:** Rev B parts arrived in time. Integration testing started on schedule. The runtime check caught one instance where a rev A board was accidentally used in testing, preventing a misleading bug report. The incident led to a new checklist item in our hardware-software interface review process.

---

### Story 4 – Failure and Learning (OTA Regression)

**Situation:** During a scheduled OTA firmware update campaign for a fleet validation build at General Motors, a regression caused approximately 12% of ECUs to fail the update and roll back to the previous version. The failure was silent — units reported success initially but then rolled back on the next power cycle.

**Task:** I was on call for the OTA system and responsible for finding the root cause, stopping the campaign from affecting more units, and preventing recurrence.

**Action:**
1. Immediately paused the campaign. Analyzed the logs from affected units: the update completed, the hash check passed, but the boot flag was not being written atomically — a power glitch during the flag write left it in a partially written state that the bootloader interpreted as "update failed."
2. Root cause: I had recently optimized the flash write routine to reduce write cycles, but changed it from a multi-byte write (atomic at the controller level) to a single-byte write loop. The optimization broke the atomicity guarantee.
3. The regression was not caught because our HIL test suite simulated clean power-off between update stages, not mid-write interruptions.
4. Fix: reverted to multi-byte atomic writes for the boot flag only. Added a power-interruption emulation test to the regression suite using a relay-controlled power supply.
5. Documented the incident with a full timeline, contributing factors, fix, and prevention steps. Shared across the firmware team.

**Result:** The fix was validated in 48 hours. Remaining ECUs in the campaign updated successfully. The new power-interruption test caught two additional edge cases in subsequent builds before they reached fleet hardware. I personally internalized that optimization changes to safety-critical paths require explicit review of atomicity guarantees — a standard I now apply proactively when touching bootloader or OTA code at any company.

---

## 11. Quick Reference Cheat Sheet

### 11.1 – ARM / Embedded Memory Layout

| Region | Content | Initialized by | Notes |
|---|---|---|---|
| `.text` | Executable code | — | Read-only; in flash |
| `.rodata` | String literals, `const` globals | — | Read-only; in flash |
| `.data` | Initialized global/static vars | Startup code copies from flash | In RAM at runtime |
| `.bss` | Uninitialized global/static vars | Startup code zeroes this region | In RAM; no flash copy |
| Heap | `malloc`/`free` allocations | Runtime | Grows upward |
| Stack | Function frames, local vars | CPU | Grows downward; each RTOS task has its own |

A `static` local variable lives in `.bss` (if zero-initialized) or `.data` (if initialized), not on the stack.

---

### 11.2 – Synchronization Primitive Comparison

| Primitive | Ownership | Priority Inheritance | Blocking | Best Use Case |
|---|---|---|---|---|
| Mutex | Yes (locker must unlock) | Yes (typically) | Yes (sleeps) | Protecting a shared data structure |
| Binary Semaphore | No | No | Yes | Task-to-task signaling |
| Counting Semaphore | No | No | Yes | Resource pool of N units |
| Spinlock | Yes | No | No (busy-wait) | Very short critical sections, interrupt context |
| Condition Variable | No | No | Yes | Wait-until-condition with associated mutex |
| Reader-Writer Lock | Shared/Exclusive | Varies | Yes | Read-heavy shared data (many readers, rare writers) |

---

### 11.3 – IPC Mechanism Comparison

| Mechanism | Latency | Overhead | Data Size | Best Use Case |
|---|---|---|---|---|
| Shared memory | Lowest | Low (cache ops) | Any | High-bandwidth CPU↔DSP/NPU buffers |
| Message queue | Low–Medium | Medium | Small–Medium | Structured command passing, ownership transfer |
| Mailbox | Very low | Very low | 1–4 words | Doorbell + small payload (pointer/length) |
| Doorbell (MMIO write) | Lowest (register write) | Minimal | 0 (signal only) | Notification after shared memory write |
| Pipe (Linux) | Medium | Kernel copy | Any | User-space producer-consumer |

---

### 11.4 – ARM Cache Operation Reference

| Operation | ARM Instruction | When to Use |
|---|---|---|
| Clean (write back) | `DC CVAC` (to PoC) | Before DMA reads CPU-written buffer; before sharing with non-coherent core |
| Invalidate | `DC IVAC` | After DMA writes result buffer; before CPU reads it |
| Clean + Invalidate | `DC CIVAC` | When the buffer will be both read and reused; or at end of shared ownership |
| Instruction sync | `ISB` | After modifying code or exception vectors |
| Data sync barrier | `DSB SY` | After cache ops, before signaling another core / hardware |
| Data memory barrier | `DMB SY` | Ordering loads/stores without completing previous ops |

**Rule of thumb:** CPU→DMA: clean before start. DMA→CPU: invalidate after completion. Add `DSB SY` after any cache operation before the handshake flag write.

---

### 11.5 – Common Bit Tricks (Embedded Interview Classics)

```c
// Clear lowest set bit
n = n & (n - 1);

// Isolate lowest set bit
lowest = n & (-n);

// Check if power of two
int is_pow2 = (n > 0) && ((n & (n - 1)) == 0);

// Toggle bit at position k
n ^= (1u << k);

// Set bit at position k
n |= (1u << k);

// Clear bit at position k
n &= ~(1u << k);

// Extract field: bits [high:low]
uint32_t field = (reg >> low) & ((1u << (high - low + 1)) - 1);

// Swap two integers without a temporary
a ^= b; b ^= a; a ^= b;

// Round up to next power of two (32-bit)
n--;
n |= n >> 1; n |= n >> 2; n |= n >> 4; n |= n >> 8; n |= n >> 16;
n++;
```

---

### 11.6 – Deadlock Prevention Quick Reference

| Technique | How | Trade-off |
|---|---|---|
| Lock ordering | Always acquire locks A before B across all threads | Requires global convention; breaks with dynamic lock sets |
| Try-lock with timeout | `mutex_trylock(m, timeout)` — release held locks and retry | Risk of livelock if all threads retry simultaneously |
| Lock-free structures | Atomic CAS operations, no locks | Complex to design and verify |
| Resource hierarchy | Number all resources; acquire in ascending order | Same as lock ordering; formal proof available |
| Avoid hold-and-wait | Acquire all locks at once (atomic multi-lock) | Reduces parallelism |

---

<div align="center">⁂</div>

[^1]: https://dataford.io/interview-guides/qualcomm/software-engineer
[^2]: https://www.glassdoor.co.in/Interview/Qualcomm-AI-platform-software-engineer-Interview-Questions-EI_IE640.0,8_KO9,38.htm
[^3]: https://interviewignition.com/companies/qualcomm/interview/
[^4]: https://www.jointaro.com/interviews/companies/qualcomm/experiences/software-engineer-audio-dsp-united-states-june-1-2017-no-offer-positive-a7f3ddfd/
[^5]: https://www.glassdoor.co.in/Interview/Qualcomm-Interview-Questions-E640.htm
[^6]: https://www.youtube.com/watch?v=AFyLajdaevg
[^7]: https://www.geeksforgeeks.org/interview-experiences/qualcomm-interview-set-2/
[^8]: https://github.com/theEmbeddedGeorge/theEmbeddedNewTestament.github.io/blob/master/Interview/Company/qualcomm.md
[^9]: https://www.geeksforgeeks.org/interview-experiences/qualcomm-interview-experience-for-ml-and-system-engineer/
[^10]: https://www.geeksforgeeks.org/qualcomm-interview-set-2/
[^11]: https://www.glassdoor.co.in/Interview/Qualcomm-Audio-DSP-Engineer-Interview-Questions-EI_IE640.0,8_KO9,27.htm
[^12]: https://www.lets-code.co.in/previousyearcodingquestion/qualcomm-previous-year-coding-questions/
[^13]: https://www.vervecopilot.com/interview-questions/top-30-most-common-embedded-c-interview-questions-you-should-prepare-for
[^14]: https://www.ccbp.in/blog/articles/embedded-c-interview-questions
[^15]: https://medium.com/@PranabNandy/qualcomm-interview-experience-2e0edc562d42
[^16]: https://www.studocu.com/in/document/jawaharlal-nehru-technological-university-kakinada/managerial-economics/embedded-systems-internship-technical-qa-moship-interview-prep/144123895
[^17]: https://www.vervecopilot.com/interview-questions/top-30-most-common-embedded-software-interview-questions-you-should-prepare-for
[^18]: https://climbtheladder.com/jtag-interview-questions/
[^19]: https://www.interviewquestionspdf.com/2023/11/24-jtag-interview-questions-and-answers.html
[^20]: https://www.glassdoor.co.in/Interview/Qualcomm-DSP-Engineer-Interview-Questions-EI_IE640.0,8_KO9,21.htm
[^21]: https://www.cleverprep.com/companies/qualcomm/dsp-engineer
[^22]: https://www.reddit.com/r/ComputerEngineering/comments/1pby3s9/embedded_dsp_software_engineer_interview/
[^23]: https://www.rfwireless-world.com/interview-qa/dsp-processor-interview-questions-and-answers
[^24]: https://www.jointaro.com/interviews/companies/qualcomm/experiences/dsp-software-engineer-united-states-october-23-2025-no-offer-neutral-4f867dc1/
[^25]: https://www.geeksforgeeks.org/interview-experiences/qualcomm-interview-experience-for-embedded-system/
[^26]: https://www.glassdoor.co.in/Interview/Qualcomm-Qualcomm-Embedded-Engineer-Interview-Questions-EI_IE640.0,8_KO9,26.htm
[^27]: https://www.linkedin.com/posts/amrit5_sharing-qualcomm-1st-round-interview-questions-activity-7083330295042617345-T8C9
[^28]: https://www.glassdoor.com/Interview/Qualcomm-AI-platform-software-engineer-Interview-Questions-EI_IE640.0,8_KO9,38.htm
[^29]: https://medium.com/interview-preparation/my-qualcomm-interview-experience-for-sr-engineer-sr-702e8156d2d1
[^30]: https://www.jointaro.com/interviews/companies/qualcomm/experiences/dsp-firmware-engineer-hyderabad-october-1-2016-no-offer-positive-38eb3661/
[^31]: https://www.scribd.com/document/433846811/interview-questions
