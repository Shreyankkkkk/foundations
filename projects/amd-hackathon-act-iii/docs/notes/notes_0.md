# AMD Developer Hackathon — ACT III

## Preliminary Research Notes: AMD Hardware, AI Software, and Technical Limitations

**Research date:** 10 October 2026

**Purpose:** Understand what technology we can use for the hackathon, what has been demonstrated to work, and what still needs to be checked before choosing a project.

These are learning notes, not the research report itself. The goal is to understand the concepts well enough to discuss the options and limitations with the team.

---

## 1. The basic idea: how AI runs on AMD hardware

To understand the research, we need to distinguish four things.

### 1.1 Hardware — what actually does the work?

A GPU is a processor that can perform many calculations in parallel. GPUs are useful for AI because running AI models involves enormous numbers of calculations.

AMD has several types of hardware:

- **AMD Instinct MI200, MI300, and MI350:** GPUs designed for data centres and demanding AI workloads.
- **AMD Radeon RX 7900 and RX 9000:** graphics cards intended primarily for consumer computers, which can also run supported AI workloads.
- **AMD Ryzen AI MAX and AI 300:** computer processors designed for PCs, with integrated graphics and a focus on local AI capabilities.

These are different hardware product families. Support for one does not automatically mean the same setup works on another.

### 1.2 ROCm — software that lets applications use AMD GPUs

ROCm is AMD's GPU computing software platform.

Think of it as the software foundation that allows compatible AI applications to use AMD GPU hardware.

**ROCm is not the GPU itself, and it is not the cloud service that gives us access to a GPU.**

For example:

- AMD Instinct MI300X = the hardware.
- ROCm = the software platform that enables supported programs to use that hardware.
- vLLM = software that can run and serve AI models using supported hardware.
- Our application = the project we build on top of these components.

### 1.3 AMD Developer Cloud — access to remote hardware

AMD Developer Cloud provides access to AMD computing hardware through the cloud.

Instead of needing to own a powerful GPU, we can potentially rent access to one remotely.

The research identified these MI300X options:

| Option | GPU configuration | Combined GPU memory |
| ------ | ----------------- | ------------------: |
| Small  | 1 × MI300X        |              192 GB |
| Large  | 8 × MI300X        |            1,536 GB |

**GPU memory** is the memory available to hold model parameters and other data while the GPU works. It is not the same as storage space on a hard drive.

The 1,536 GB figure is the combined GPU memory across eight GPUs, not one giant GPU. The model and software must be configured to use multiple GPUs appropriately.

The report also references AMD's ROCm 7 performance results. Those results and the cloud hardware options are evidence that AMD provides infrastructure for substantial AI workloads, but they do not guarantee that every project will run equally well.

### 1.4 vLLM — software for running AI models

vLLM is software used to run AI models and make them available for applications to use.

For example, our application could send a question to a model running through vLLM and receive a response.

This is especially useful when we want to use an existing trained model rather than build an AI model from scratch.

One important distinction:

- **Model:** the trained AI that performs a task.
- **vLLM:** software that helps run and serve compatible models.
- **ROCm:** the platform that enables compatible software to use AMD GPUs.

---

## 2. What the research verified about AMD compatibility

The report checked official vLLM documentation for supported AMD hardware.

The documented hardware families include:

| AMD hardware          | Architecture identifier | Minimum ROCm version listed in the report |
| --------------------- | ----------------------- | ----------------------------------------- |
| Instinct MI200        | gfx90a                  | 6.3+                                      |
| Instinct MI300        | gfx942                  | 6.3+                                      |
| Instinct MI350        | gfx950                  | 7.0+                                      |
| Radeon RX 7900        | gfx1100 / gfx1101       | 6.3+                                      |
| Radeon RX 9000        | gfx1200 / gfx1201       | 6.3+                                      |
| Ryzen AI MAX / AI 300 | gfx1151 / gfx1150       | 7.0.2+                                    |

_These are the requirements reported for the particular vLLM installation documentation that was examined. They should not be treated as universal requirements for every AI application or every ROCm setup._

### What are the `gfx` numbers?

Names such as `gfx942` and `gfx950` are identifiers for GPU architectures. They help software identify the underlying hardware.

They are not separate GPU products or software packages.

For the hackathon, we should focus first on the actual GPU available to us and whether the software supports it. We do not need to memorise all these identifiers.

### Python version warning

The research found a specific installation requirement for **pre-built ROCm vLLM wheels**.

A _wheel_ is a pre-packaged Python software component that can be installed without building the package from source yourself.

For the documented pre-built ROCm wheels, Python 3.12 is required. Using Python 3.10 or 3.11 through that particular installation route can lead to the wrong package being selected and an error such as `libcudart.so` missing.

CUDA is NVIDIA's GPU computing platform; ROCm is AMD's.

This does **not** mean every AMD AI application requires Python 3.12. It means we must check the installation instructions for the exact software we choose.

**Practical lesson:** Before installing a model-serving setup, confirm the GPU, ROCm version, Python version, and supported package version together. A mismatch can prevent the software from running even when the hardware itself is compatible.

---

## 3. AI models: what can we actually build with?

An AI model is trained to perform a task. Different model types have different capabilities.

### 3.1 Large language models (LLMs)

An LLM works primarily with language. It can perform tasks such as:

- Answering questions.
- Summarising documents.
- Explaining information.
- Generating and rewriting text.
- Processing text-based customer support requests.

A language model could be useful for projects involving document search, support automation, or simplifying complicated information.

### 3.2 Vision-language models (VLMs)

A VLM can work with images as well as language.

For example, it might receive a picture of a damaged component and answer questions about what is visible.

Depending on the particular model, a system may also support video or audio. **Not every VLM supports every type of input.**

The report found that vLLM's supported-model documentation lists families including Qwen-VL, LLaVA, Aria, BLIP-2, Bee, Command-A Vision, and Cosmos3, among others.

This is useful because it gives us potential models to investigate for projects involving visual information.

However, the existence of a model family on a general support list does not establish that every version of that model works on every AMD GPU.

### 3.3 Speech recognition, translation, and text-to-speech

These are separate tasks that can be combined into a single system.

| Component               | What it does                                                                   |
| ----------------------- | ------------------------------------------------------------------------------ |
| Whisper                 | Converts spoken audio into text.                                               |
| Translation model       | Converts text from one language into another.                                  |
| TTS (text-to-speech)    | Converts text into spoken audio.                                               |
| Speech-to-speech system | Takes spoken audio and produces spoken audio, potentially in another language. |

For example, a multilingual communication application could work like this:

1. A person speaks in one language.
2. Speech recognition converts the audio into text.
3. A translation model translates the text.
4. TTS converts the translated text into speech.
5. The other person hears the translated audio.

A **pipeline** is simply a sequence of steps in which one component's output becomes another component's input. It is not necessarily a special AI model or a routing mechanism.

---

## 4. What has actually been tested, and what has not?

This is one of the most important distinctions in the report.

There is a difference between software being supported in general, a particular model being documented, and the complete application being tested.

| Evidence level                  | What it means                                                            |
| ------------------------------- | ------------------------------------------------------------------------ |
| General support documented      | The software claims to support the technology or category.               |
| Specific integration documented | Documentation covers the particular model and setup.                     |
| End-to-end test completed       | The complete setup was run to check that it works for the intended task. |

### Example

Suppose vLLM documents support for multimodal models on ROCm.

That is encouraging. However, it does not prove that our exact chosen model and version will install correctly, process images properly, and produce the outputs we need on our chosen AMD GPU.

The correct conclusion is not that the model will fail. It is that we have not yet established that the exact setup works.

For any model we choose, we should check:

- Is the specific model supported?
- Is our GPU supported?
- Are the software and Python versions compatible?
- Can the model perform the task we need?
- Has the complete setup been tested, or is it still a candidate?

Until those questions are answered, the model integration should be labelled **candidate, untested** rather than end-to-end verified.

---

## 5. AMD's published performance results

The report identified two sets of relevant performance evidence.

### 5.1 ROCm 7 performance results

AMD's ROCm 7 announcement reported:

- More than 3.5× inference performance improvement in specific tested workloads.
- A 3× training performance improvement in a test using Megatron-LM across eight MI300X GPUs.

The inference tests referenced models and configurations including Llama 3.1-70B, Qwen 72B, and DeepSeek-R1.

Some terminology:

- **Inference:** running an already-trained model to produce an answer or other output.
- **Training:** using data to adjust a model's parameters so it learns.
- **70B / 72B:** approximately 70 billion or 72 billion model parameters.
- **FP16:** a 16-bit floating-point number format used in AI calculations.
- **TP2:** tensor parallelism across two GPUs. In simple terms, parts of the model's calculations are split across two GPUs.
- **Megatron-LM:** software used to train large AI models across multiple GPUs.

These results show that AMD's hardware and software can deliver substantial performance for the specific workloads tested.

However, a result of more than 3.5× does **not** mean our application will automatically run 3.5 times faster. Performance depends on the model, software, hardware configuration, and workload being tested.

For our hackathon, we should care more about whether our chosen project runs correctly and fast enough than about a headline benchmark from a different workload.

### 5.2 vLLM ROCm attention-backend benchmarks

The report also identified a vLLM benchmark comparing different software components responsible for part of an AI model's calculations.

The tests covered:

- MI300X, with 192 GB of GPU memory.
- MI325X, with 256 GB.
- MI355X, with 288 GB.

The models included Qwen3-235B-A22B-FP8 and DeepSeek-R1-0528.

Some terms:

- **Attention:** a mechanism that helps an AI model determine which parts of its input are relevant when processing information.
- **MHA:** multi-head attention, a common attention design.
- **MLA:** multi-head latent attention, an alternative attention design.
- **FP8:** an 8-bit floating-point number format.
- **235B:** approximately 235 billion total model parameters.
- **A22B:** approximately 22 billion active parameters per token for the referenced model configuration.

The benchmark used `ROCM_AITER_FA` as its reference backend. In the tested configurations, `ROCM_ATTN` was reported to be 3.6–4.4 times slower than that reference.

A **backend** here is the software implementation that performs a particular calculation. This benchmark compares software implementations on AMD hardware, not AMD GPUs against NVIDIA GPUs.

The report also noted that another backend had a lower relative value than the reference in one configuration. Without the exact metric and table context, we should not assume whether that lower number represents better or worse performance.

### What does the benchmark tell us about VLMs?

The benchmark did not include vision-language models.

That means it does not establish the image/video processing throughput of those models under the tested conditions.

It does **not** mean AMD cannot run VLMs. It means this particular benchmark is not evidence of how fast a VLM will run.

---

## 6. Limitations and gaps identified by the research

These are the uncertainties we should keep in mind before choosing our project architecture.

### 6.1 Speech pipeline support on ROCm is not specifically verified

The inference documentation examined by the report discusses general routes through tools such as Hugging Face Transformers and vLLM. The research did not find a specifically documented end-to-end Whisper, speech-to-speech, or TTS pipeline in that material.

This does not prove those components cannot run on AMD hardware. It means this particular research has not established the exact setup and its compatibility.

**What this means for project selection:** A speech-heavy project may still be possible, but we would need to verify each component and test the complete pipeline. We should not assume that a working text model automatically proves the speech components will work.

### 6.2 Not every component necessarily needs to run on AMD

The hackathon brief says a meaningful part of the workload must run on AMD hardware.

One possible interpretation is that some components can run elsewhere, provided the AMD component performs meaningful work. For example:

- A VLM or translation model runs on an AMD Instinct GPU.
- TTS synthesis runs on another machine or service.

That is a plausible candidate architecture, but the research has not independently confirmed that this exact implementation meets the event's eligibility requirements.

**Important:** We must not assume that 75% of the workload is a confirmed threshold. The 75% figure is only a hypothetical example, not a rule established by the research. If our project depends on splitting work between AMD and other hardware, we should clarify the requirement with the organisers.

### 6.3 General compatibility is not proof of our exact setup

Even if vLLM supports ROCm and lists a model family, we still need to verify the specific model and version.

This matters because a project can look technically feasible on paper but fail during setup because of an incompatible package, unsupported model feature, or missing integration.

The right response is to perform a small proof of concept before committing to a project.

### 6.4 GPU availability and quota during the event are unconfirmed

The report did not establish whether the required GPU instances would be available during the event week or what usage limits would apply.

A quota is a limit on resource usage. For example, access might be limited by GPU hours, the number of instances, or which hardware types can be requested.

Cloud credits do not necessarily guarantee unlimited GPU access or availability of every instance type.

**What this means for project selection:** We need to confirm access, limits, and the intended GPU configuration before designing a project that depends on a particular machine.

---

## 7. How to interpret the research before exploring the hackathon tracks

The preliminary report is not choosing a project. It is establishing the technical options and constraints that should inform our later decisions.

For example:

- If we choose an image-understanding project, a VLM is a potential approach.
- If we choose a multilingual communication project, speech recognition, translation, and TTS could form a pipeline.
- If we choose a document or support automation project, an LLM may be sufficient.
- If we choose a project involving several components, we must decide which components run on AMD and verify that the overall design satisfies the event's rules.

The most important question is not simply whether a model exists. It is whether we can run the required parts of our chosen system, within the event's constraints, and demonstrate a working result.

---

## Key takeaways for the team discussion

### Pros

- **AMD AI infrastructure is available:** the research identified MI300X cloud options and documented software support for several AMD hardware families.
- **There are multiple model options:** vLLM's supported-model documentation lists a variety of language and multimodal model families.
- **We can potentially use existing trained models:** we do not necessarily need to train an AI model from scratch.
- **Some workloads have encouraging published performance results:** AMD and vLLM have published benchmarks, although their results apply to specific configurations.
- **We may have architectural flexibility:** some components could potentially run outside AMD hardware if the organisers accept the design and the AMD portion is meaningful.

### Cons and limitations

- **General support does not guarantee our chosen model works:** we must verify the exact model, version, software stack, and hardware.
- **Speech-related integration remains an open question in this research:** the exact Whisper/translation/TTS route has not been verified end to end.
- **Published benchmark numbers are not guarantees:** results from large models and specific configurations may not represent our application.
- **Event-week access is not confirmed:** GPU availability, quota, and limits need checking.
- **The precise meaning of “meaningful part” needs care:** we must not invent a percentage threshold or assume our architecture is eligible without evidence.

### Questions to resolve before committing to a project

1. Which AMD GPU and cloud instance will we actually be able to access during the event?
2. What usage limits or quotas apply?
3. Does our chosen model run on that hardware with a compatible software setup?
4. If we use speech, vision, or multiple AI components, can we demonstrate that the complete pipeline works?
5. If some components run outside AMD, do the organisers accept that specific design as meeting the “meaningful workload” requirement?

**Bottom line:** The research establishes that AMD has viable AI hardware and a documented software ecosystem. It does not establish that every model or pipeline we might want to build is ready to use, nor that the required cloud resources will definitely be available. We should treat promising approaches as candidates until we verify them with a small working test.

---

## Key Takeaways for the Team Discussion

### What we can potentially build

- **LLM-based application:** A promising starting point. We can use an existing language model to build something useful without training a model from scratch.
- **Image-understanding application:** Also promising. We can investigate a vision-language model (VLM) that runs on AMD hardware.
- **Speech-based application:** Possible, but less certain. Whisper, translation, and text-to-speech components need to be checked and tested.
- **Multi-component AI application:** Components may potentially run on different hardware, but we need to confirm that our design satisfies the hackathon's AMD workload requirement.

### Advantages

- AMD provides AI-focused GPUs, including MI300X cloud instances.
- vLLM documents support for various language and multimodal model families.
- We can potentially build around existing trained models instead of training one ourselves.
- Published benchmarks show promising performance for certain AMD workloads.
- We have several possible technical approaches to explore before choosing a project.

### Limitations and risks

- **Model compatibility:** General software support does not guarantee that our exact model and version will work.
- **Speech integration:** Our research has not verified a complete Whisper-to-translation-to-TTS pipeline on AMD.
- **Performance:** Published benchmark results do not guarantee similar performance for our project.
- **Cloud access:** GPU availability, usage quotas, and access during the event remain unconfirmed.
- **Hackathon eligibility:** We must confirm what qualifies as a meaningful workload on AMD. We cannot assume a particular percentage is sufficient or that every split-hardware design will be accepted.

### What we need to verify

1. **Hardware access:** Which AMD GPU can we actually use during the event, and what are its usage limits?
2. **Model compatibility:** Can our chosen model run on that GPU with the required software?
3. **Working implementation:** Can we

## Sources and Evidence

**Research date: 10 October 2026**

### 1. Official vLLM ROCm Installation Documentation

**Source:** [vLLM — GPU Installation Guide](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html)

**Supports:**

- AMD hardware architectures supported by the documented vLLM ROCm installation paths.
- ROCm version requirements for the listed hardware.
- Installation instructions and available pre-built ROCm wheels.
- Python version requirements for the particular installation method.

**Why it matters:** Use this source to check whether our chosen AMD GPU and software environment are compatible before attempting installation.

**Important limitation:** These requirements apply to the documented vLLM installation route, not necessarily every AI application running on AMD hardware.

### 2. Official vLLM Supported Models Documentation

**Source:** [vLLM — Supported Models](https://docs.vllm.ai/en/latest/models/supported_models.html)

**Supports:**

- Model families supported by vLLM.
- Documented language and multimodal model integrations.
- Potential model choices for text-based and image-understanding applications.

**Why it matters:** This is where we can investigate whether a model we want to use has a documented vLLM integration.

**Important limitation:** General support for a model family does not guarantee that every model version works with our chosen GPU, ROCm version, and software configuration.

### 3. AMD ROCm 7 and AMD Developer Cloud

**Source:** [AMD — Enabling the Future of AI: Introducing AMD ROCm 7 and the AMD Developer Cloud](https://www.amd.com/en/blogs/2025/enabling-the-future-of-ai-introducing-amd-rocm-7-and-the-amd-developer-cloud.html)

**Supports:**

- Information about AMD Developer Cloud and MI300X GPU configurations.
- AMD's published ROCm 7 inference performance results.
- Published training performance results using Megatron-LM on multiple MI300X GPUs.

**Why it matters:** This provides evidence that AMD offers cloud infrastructure and has demonstrated substantial performance on particular AI workloads.

**Important limitation:** Published benchmark results apply to the configurations tested. They do not guarantee the same performance for our project or confirm that cloud resources will be available during the hackathon.

### 4. vLLM ROCm Attention Backend Benchmarks

**Source:** [vLLM — ROCm Attention Backend Benchmarks, 27 February 2026](https://vllm.ai/blog/2026-02-27-rocm-attention-backend)

**Supports:**

- The AMD GPUs and AI models included in the reported benchmarks.
- Comparisons between attention software backends.
- The reported performance differences between the tested implementations.

**Why it matters:** It helps us understand that software implementation choices can significantly affect AI performance, even when the underlying hardware is the same.

**Important limitation:** The benchmark did not include vision-language models, so it does not establish their image-understanding throughput.

---

## Unverified Items and Research Gaps

The following items were identified as gaps in the research. They should not be treated as confirmed technical limitations.

| Open question | What remains unverified | Next step |
| --------------------------------------------------- |
| Whisper and speech recognition on ROCm | The specific speech-recognition setup we might use has not been verified by the documentation examined.              | Investigate the chosen implementation and test it on the intended AMD hardware. |
| Text-to-speech and speech-to-speech    | A complete speech pipeline has not been established by this research.                                                | Test the individual components and then the complete pipeline.                  |
| Running some components outside AMD    | Whether a particular split-hardware architecture satisfies the hackathon rules has not been independently confirmed. | Check the official rules or ask the organisers.                                 |
| Exact model compatibility              | General vLLM support does not establish that every model/version combination works.                                  | Verify the exact model and run a proof of concept.                              |
| Event-week GPU access                  | GPU instance availability and usage quotas were not confirmed by the research.                                       | Check the event's cloud-access arrangements and applicable limits.              |

**Note:** The gaps above describe what this research did not establish. They do not prove that the technologies are unsupported or impossible to use.

The official sources above support the documented compatibility, model-support, cloud, and benchmark claims. The remaining items require further verification rather than assumptions.
