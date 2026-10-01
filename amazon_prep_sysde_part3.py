# -*- coding: utf-8 -*-
"""
Amazon Advertising in Live Events - AI Engineer Preparation
Part 2C: System Design Questions 21 to 30
All sections written in small, conversational paragraph chunks without ANY bullet points.
Candidate: Ashutosh Rudraksh
"""

from amazon_prep_sysde_part1 import generate_svg

sysde_questions_part3 = [
    # Q21: Real-Time Ad CTR/CVR Prediction Model Serving Architecture
    {
        "id": 21,
        "title": "Scalable Model Serving Architecture for Real-Time Ad CTR and CVR Prediction",
        "category": "Machine Learning & Model Serving",
        "problem_statement": """Design a high-throughput, ultra-low latency machine learning model serving architecture for real-time Click-Through Rate (CTR) and Conversion Rate (CVR) prediction in Amazon Advertising. The system must evaluate thousands of candidate ad creatives against complex viewer and contextual features, returning calibrated probability scores within eight milliseconds to power live sports ad auctions.""",
        "clarifying_questions": """When clarifying this ML serving system, I would first ask about the model architecture and size. Are we serving a deep neural network such as a Deep & Cross Network (DCN) or Deep Interest Network (DIN), or a gradient boosted decision tree? In modern advertising, a two-stage hybrid approach is common: a lightweight retrieval filter followed by a deep neural ranking model running on optimized hardware.

Next, I would ask about the candidate set size per ad request. How many candidate ads must be scored per auction? If an ad request requires scoring five hundred candidate ads, scoring them sequentially will breach our eight-millisecond SLA, so batched vectorized scoring and GPU or AWS Inferentia acceleration are required.

I would also clarify the feature store architecture: how are dense user embeddings and real-time contextual features fetched and joined before inference without introducing network latency bottlenecks?

Finally, I would ask how model updates are deployed: we need zero-downtime hot swapping of model weights during live games as models are continuously updated with intraday feedback.""",
        "svg_diagram": generate_svg(
            "Real-Time CTR/CVR Model Serving Fleet",
            [
                ["Ad Auction Request", "500 Candidate Ads"],
                ["Low-Latency Feature Store", "Redis / Feast In-Memory"],
                ["Triton Inference Server", "TensorRT / AWS Inferentia"],
                ["Calibrated CTR/CVR", "Sub-8ms Batch Scoring"],
                ["Auction Ranker Engine", "eCPM Value Selection"]
            ]
        ),
        "functional_requirements": """Functionally, the serving system must accept a scoring request containing the viewer context, live broadcast attributes, and a candidate list of hundreds of eligible ad creatives.

It must retrieve real-time and pre-computed features from an in-memory feature store, including user historical engagement rates, advertiser category affinities, and live game contextual tags.

The system must assemble feature tensors and feed them into deep neural ranking models compiled for hardware acceleration.

It must output calibrated Click-Through Rate and Conversion Rate probabilities for every candidate ad within eight milliseconds.

Finally, it must log inference features and predictions to an asynchronous event stream to support model evaluation, continuous training pipelines, and data drift monitoring.""",
        "non_functional_requirements": """From a non-functional perspective, P99 inference latency must not exceed eight milliseconds, as this scoring step is a critical component of the overall forty-millisecond auction SLA.

The serving cluster must sustain over five hundred thousand inference requests per second during peak commercial break transitions across live sporting events.

Model availability must be 99.999 percent, with graceful fallback to heuristic scoring if an inference worker experiences hardware degradation.

The architecture must support dynamic model hot-swapping without dropping active requests or causing memory thrashing.""",
        "core_entities": """The primary core entity is the Scoring Request, containing the auction ID, viewer identifier, slot duration, and candidate creative IDs.

Next is the Feature Vector Bundle, combining static user features, dynamic real-time contextual features, and creative embedding tensors.

We also have the Deep Ranking Model Artifact, representing the compiled TensorRT or AWS Neuron model binary, neural network weights, and preprocessing metadata.

Another entity is the Calibrated Prediction Output, capturing the estimated CTR, estimated CVR, and uncertainty interval for each candidate.

Finally, the Model Performance Telemetry entity tracks prediction latency distributions, throughput, GPU utilization, and feature drift metrics.""",
        "api_design": """The model serving layer implements an ultra-fast internal gRPC endpoint called /v1/models/ad_ranker:predict utilizing Protocol Buffers for minimal serialization overhead.

The request payload accepts the user feature key and an array of creative identifiers, returning an array of floating-point probabilities.

An internal model management API allows MLOps engineers to deploy new model versions, initiate canary traffic splits, and rollback versions instantly.

A feature ingestion API continuously streams real-time interaction features into the feature store from upstream Kafka click and impression topics.""",
        "data_flow": """The data flow begins when the ad auction engine identifies a pool of eligible candidate creatives and dispatches a scoring request to the nearest model serving pod.

The serving worker queries an in-memory Redis feature store using the user ID, retrieving the user's dense embedding vector and recent category interaction counts in under one millisecond.

The worker concatenates the user features, creative features, and live game context into a batched input tensor.

The tensor is dispatched to an NVIDIA GPU or AWS Inferentia chip running Triton Inference Server, which executes the deep ranking model across all candidate ads in parallel.

The model outputs raw logits, which are passed through a calibration function to produce true probabilities, and the ranked candidate scores are returned to the auction engine in under six milliseconds.""",
        "high_level_design": """At a high level, the architecture combines a high-speed feature retrieval layer, a distributed model inference fleet, and an asynchronous telemetry feedback loop.

Feature retrieval is anchored by an in-memory Redis cluster or Feast feature store deployed locally within each AWS region to ensure microsecond read latencies.

The inference fleet utilizes Triton Inference Server running on GPU-accelerated EC2 instances or AWS Inferentia2 instances, managed within an Auto Scaling Amazon EKS cluster.

Models are trained offline using PyTorch and compiled into highly optimized TensorRT or AWS Neuron engines to maximize hardware throughput and minimize compute latency.

Prediction logs are emitted asynchronously via Amazon Kinesis to an S3 feature store bucket, providing ground-truth training datasets for continuous model improvement.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, maintaining sub-eight-millisecond latency for batches of five hundred candidate ads requires deep architectural optimizations. We eliminate cross-network feature fetching by using Shared Memory and in-process feature caching: frequently accessed creative embeddings are held directly in the RAM of the inference host, requiring zero network calls to construct the creative half of the input tensor.

To maximize hardware efficiency on GPUs, Triton Inference Server uses Dynamic Batching with a two-millisecond queuing window, grouping incoming concurrent requests together to fully saturate GPU tensor cores without breaching the latency SLA.

To protect live broadcasts from inference server crashes, we implement an automated Local Heuristic Fallback: if an inference pod fails to return predictions within seven milliseconds, the auction engine immediately scores candidates using a lightweight, CPU-based logistic regression model running locally within the auction process.

Model deployment utilizes Blue-Green Model Hot-Swapping inside Triton: new model weights are loaded into GPU VRAM in the background and verified with synthetic warm-up queries before live auction traffic is transitioned, guaranteeing zero dropped requests during live sports events.""",
    },

    # Q22: Real-Time Ad Fraud, Bot Traffic & Invalid Traffic (IVT) Filtering
    {
        "id": 22,
        "title": "Real-Time Ad Fraud, Bot Traffic, and Invalid Traffic Filtering Engine",
        "category": "Security & Fraud Detection",
        "problem_statement": """Design a real-time Invalid Traffic (IVT) and ad fraud filtering engine for Prime Video advertising. The system must analyze billions of daily ad requests and impression beacons, detecting sophisticated botnets, headless browser emulators, click farms, and fraudulent impression generators with sub-ten-millisecond latency to ensure advertisers only pay for verified human views.""",
        "clarifying_questions": """To clarify this fraud detection system, I would first ask about the types of Invalid Traffic we are targeting: are we focusing primarily on General Invalid Traffic (GIVT) like known web crawlers, data center IP ranges, and search engine bots, or Sophisticated Invalid Traffic (SIVT) like residential proxy botnets, headless browser emulators, and session hijacking? Both GIVT and SIVT detection are necessary to achieve Media Rating Council accreditation.

Next, I would ask where in the request lifecycle filtering occurs. Does it filter ad requests before auctions run, filter impression beacons after playback, or both? Filtering pre-bid prevents wasted auction compute, while post-impression verification prevents billing fraud.

I would also clarify the acceptable false positive rate. In live sports on Prime Video, legitimate human viewers occasionally exhibit bursty behavior (such as refreshing the stream rapidly during a game-winning play); we must ensure legitimate paying subscribers are never erroneously blocked.

Finally, I would ask about telemetry signals available from the video player SDK, such as client sensor data, behavioral mouse/touch dynamics, and cryptographically attested device integrity tokens.""",
        "svg_diagram": generate_svg(
            "Real-Time IVT & Ad Fraud Filtering Engine",
            [
                ["Incoming Ad/Beacon", "Client Request Stream"],
                ["GIVT Fast Filter", "IP & User-Agent Bloom"],
                ["SIVT ML Classifier", "Behavioral Anomaly Model"],
                ["Device Attestation", "App & Hardware Sig"],
                ["Decision Gateway", "Legitimate Traffic Pass"]
            ]
        ),
        "functional_requirements": """Functionally, the engine must inspect every incoming ad request and impression beacon to verify device authenticity and human interaction signals.

It must execute a fast-path General Invalid Traffic check against known data center IP ranges, public cloud subnets, and malicious botnet blacklists.

The system must verify cryptographic device attestation tokens (such as Apple DeviceCheck, Google Play Integrity, and Fire TV hardware signatures) to confirm the app has not been tampered with or run inside an emulator.

It must apply a machine learning classification model to detect Sophisticated Invalid Traffic, analyzing behavioral telemetry such as viewing patterns, session duration, and request frequency anomalies.

Finally, it must tag every ad transaction as valid or invalid, preventing fraudulent impressions from being billed and updating global fraud blacklists in near real time.""",
        "non_functional_requirements": """From a non-functional perspective, pre-bid fraud evaluation must execute in under five milliseconds to avoid delaying live ad auctions.

The system must scale to inspect over twenty million ad calls per minute during peak live broadcasts without degrading throughput.

The false positive rate must remain below 0.01 percent to ensure that genuine Prime Video viewers never have their streams interrupted or ads withheld.

Data security and compliance must adhere strictly to privacy guidelines, hashing IP addresses and device identifiers to protect user privacy.""",
        "core_entities": """The primary core entity is the Traffic Inspection Event, capturing client IP, user agent, device attestation token, session ID, and playback interaction signals.

Next is the Known Threat Intelligence Record, containing blacklisted IP CIDR blocks, known crawler signatures, and flagged residential proxy nodes.

We also have the Device Integrity Attestation, representing the cryptographically signed hardware verification payload returned by the operating system.

Another entity is the SIVT Behavioral Profile, maintaining statistical moving averages of request rates, beacon inter-arrival times, and viewing session lengths per device.

Finally, the Fraud Audit Record captures the final classification verdict, risk score breakdown, and billing exclusion status for accounting reviews.""",
        "api_design": """The service provides an ultra-fast internal gRPC inspection endpoint called /fraud/v1/evaluate-request that returns a pass/drop decision and risk score within three milliseconds.

For post-bid impression reconciliation, an asynchronous beacon verification API /fraud/v1/verify-beacon evaluates impression tokens against recorded playback signatures.

There is a threat intelligence ingestion API that continuously ingests threat feeds from commercial security partners and internal Amazon security teams.

An operational reporting API allows fraud analysts to review suspicious traffic clusters, investigate novel botnet signatures, and manually adjust risk thresholds.""",
        "data_flow": """The data flow begins when an ad request or impression beacon arrives at our edge API gateway from a client video player.

The gateway extracts the client IP and device signature, immediately testing them against in-memory Bloom filters containing millions of blacklisted IP subnets and known crawler user agents.

If the request passes the GIVT check, the gateway validates the cryptographic hardware attestation token using public key cryptography.

The request attributes are passed to a lightweight machine learning inference service that evaluates behavioral risk features against an SIVT model.

If the risk score is below the fraud threshold, the request is marked valid and forwarded to the ad decision engine; if flagged as fraudulent, the request is dropped or served a non-billable honeypot ad, and the event is logged for fraud reporting.""",
        "high_level_design": """At a high level, the architecture employs a two-tier filtering strategy combining an edge rule evaluation layer with an asynchronous stream analytics engine.

The first tier operates directly on edge proxies and API gateways using high-speed in-memory Bloom filters and Redis lookups to eliminate over ninety percent of GIVT traffic in microseconds.

The second tier consists of a cluster of Go microservices running on Kubernetes that execute cryptographic token validation and evaluate lightweight XGBoost models for SIVT detection.

An asynchronous stream processing pipeline built on Apache Flink continuously monitors global traffic patterns across Kafka topics, identifying distributed residential proxy botnets that individual request inspections cannot detect.

Detected botnet signatures and suspicious IP clusters are automatically compiled into new filter rules and propagated back to edge Bloom filters in under sixty seconds.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, maintaining sub-five-millisecond evaluation latency across millions of requests requires avoiding heavy database queries on the critical path. We store all known malicious IP ranges and crawler signatures in compact In-Memory Bloom Filters and Radix Trees deployed locally in the memory of each API gateway, allowing IP subnet checks to execute in less than one hundred microseconds.

To combat sophisticated residential proxy networks where bots hijack real home internet connections, the system evaluates Beacon Inter-Arrival Timing: automated bots typically emit tracking beacons with unnatural, millisecond-precise intervals, whereas real human viewing devices exhibit realistic network jitter and clock drift.

To maintain absolute reliability during live sporting events, the fraud filter employs a Graceful Degradation Bypass: if the ML inference cluster experiences unexpected latency spikes above four milliseconds, the system automatically bypasses the complex SIVT model and falls back to fast GIVT filtering, ensuring that live ad auctions are never stalled.

All rejected impressions and associated telemetry are immutably archived in Amazon S3, providing transparent, audit-ready evidence for advertiser billing reconciliations and Media Rating Council compliance audits.""",
    },

    # Q23: AI-Powered Synthetic Voiceover & Multilingual Dubbing Pipeline
    {
        "id": 23,
        "title": "AI-Powered Synthetic Voiceover and Multilingual Dubbing Pipeline for Live Sports Ads",
        "category": "Generative AI & Audio Engineering",
        "problem_statement": """Design an automated AI synthetic voiceover and multilingual dubbing pipeline for Amazon live events advertising. The system must ingest English video commercial creatives, automatically translate scripts into multiple target languages (such as Spanish, Portuguese, and French), synthesize natural localized voiceovers with voice cloning that preserves brand tone, and re-encode broadcast-compliant audio tracks in under five minutes.""",
        "clarifying_questions": """When clarifying this multilingual dubbing pipeline, I would first ask about the turnaround time and workflow trigger. Is this an offline creative localization pipeline that runs when advertisers upload new ad campaigns hours or days before a broadcast, or does it need to operate in real time on live commentator audio? Running as an automated creative ingestion pipeline that completes in under five minutes upon creative upload is the industry standard.

Next, I would ask about voice cloning and brand identity: do advertisers want to preserve the exact vocal timbre, pitch, and energy of the original English voice actor across Spanish and Portuguese dubs, or can we use pre-approved synthetic studio voices? Preserving the original voice actor's timbre using zero-shot voice cloning provides the most premium advertiser experience.

I would also clarify audio synchronization: how does the system handle language expansion (for example, Spanish sentences often being twenty percent longer than English sentences) to ensure the dub aligns with on-screen actors' lip movements and scene cuts?

Finally, I would ask about broadcast compliance: audio tracks must be normalized to -24 LKFS loudness standards to comply with television broadcast regulations.""",
        "svg_diagram": generate_svg(
            "AI Synthetic Voiceover & Dubbing Pipeline",
            [
                ["Ad Creative Upload", "English Master Video"],
                ["Audio Demux & Whisper", "Speech-to-Text & Diarize"],
                ["Contextual LLM Translate", "Duration-Constrained Text"],
                ["Voice Cloning TTS", "Neural Audio Synthesis"],
                ["Audio Mastering & Mux", "Broadcast -24 LKFS File"]
            ]
        ),
        "functional_requirements": """Functionally, the platform must allow advertisers and operations teams to upload master video commercial files with an original audio track.

The system must separate the audio track into speech vocals and background music or sound effects using automated audio source separation algorithms.

It must transcribe the vocal track with precise word-level timestamps using automated speech recognition models.

The system must translate the transcribed script into target languages using an LLM instructed to match the exact syllable count and timing of the original speech.

It must synthesize the translated script using a neural text-to-speech model that clones the original speaker's vocal characteristics, mix the new vocal track with the original background music, normalize audio loudness to broadcast standards, and mux the new audio back into the video file.""",
        "non_functional_requirements": """From a non-functional perspective, end-to-end processing time for a thirty-second commercial creative must be under five minutes across three target languages.

Audio quality must meet broadcast standards, exhibiting zero metallic artifacts, robotic distortions, or unnatural pronunciation of brand names.

Timing synchronization must ensure that translated speech segments stay within one hundred milliseconds of the original scene cuts and speaker appearances.

The pipeline must scale elastically to process hundreds of commercial creative submissions concurrently ahead of major global sporting events like the Olympics or World Cup.""",
        "core_entities": """The primary core entity is the Creative Localization Job, tracking the master video asset ID, source language, target languages, submission timestamp, and processing status.

Next is the Audio Track Stem, representing separated audio streams including isolated dialogue, ambient sound effects, and background musical score.

We also have the Time-Aligned Transcript, containing source text segments, word-level start and end timestamps, and speaker diarization labels.

Another entity is the Translated Script Segment, capturing the localized text, target language code, maximum allowable duration, and syllable pacing constraints.

Finally, the Mastered Localized Creative entity links the finalized multi-track video asset, transcoded bitrate variants, and loudness compliance certification.""",
        "api_design": """The service provides an asynchronous REST API endpoint /creatives/v1/localize where advertisers submit creative video URLs and select target localization languages.

An internal webhook notification service dispatches progress updates and completion events to the campaign management portal when localized assets are ready.

There is a review and approval API allowing brand managers to listen to generated audio tracks, inspect transcript side-by-side diffs, and request manual text adjustments.

A streaming monitoring API emits pipeline processing metrics, GPU utilization stats, and audio quality scores to internal engineering dashboards.""",
        "data_flow": """The data flow begins when an advertiser uploads a master commercial to Amazon S3, triggering an AWS Step Functions workflow via an Amazon S3 Event Notification.

The workflow invokes a GPU worker that uses an audio separation model like Demucs to split the soundtrack into dialogue and background stems.

An automated speech recognition model (such as Whisper) transcribes the dialogue stem, producing a timestamped transcript.

The transcript is fed into an LLM on Amazon Bedrock with a custom system prompt that translates the copy into target languages while strictly respecting original segment durations.

The translated text and original voice sample are passed to a neural voice cloning TTS model running on GPU inference nodes.

The synthesized vocal track is dynamically time-stretched to align with scene timestamps, mixed with the background music stem, normalized to -24 LKFS using an automated audio mastering filter, and multiplexed back into the video container.""",
        "high_level_design": """At a high level, the architecture is designed as an asynchronous, distributed media processing pipeline orchestrated by AWS Step Functions and AWS Batch.

Storage is anchored by Amazon S3 for raw media assets, intermediate audio stems, and finalized localized video packages.

Compute workloads are distributed across an Auto Scaling cluster of GPU-enabled EC2 instances running specialized Docker containers for audio separation, speech recognition, and neural voice synthesis.

Translation and duration matching are powered by foundation models accessible through Amazon Bedrock.

Asset metadata, processing status, and approval audit logs are persisted in Amazon Aurora PostgreSQL, with finalized creative URLs registered in the Publisher Ad Server creative catalog.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, solving the Language Expansion Problem (where translated Spanish text takes longer to speak than the original English) without causing video desynchronization requires a combination of constrained LLM prompting and intelligent audio time-stretching. During the translation phase, our LLM prompt explicitly specifies the target syllable count and maximum duration in milliseconds for each sentence, enforcing conciseness while preserving marketing punchiness.

If the synthesized audio is still slightly longer than the allotted video window, the mastering pipeline applies a Phase Vocoder time-compression algorithm that speeds up speech by up to ten percent without changing voice pitch or creating unnatural audio distortion.

To guarantee that brand names and slogans are pronounced correctly across languages, the system maintains a Brand Pronunciation Dictionary containing phonetic IPA representations that override standard phonetic rules.

Broadcast loudness compliance is strictly enforced: every mastered audio file passes through an automated ITU-R BS.1770-4 loudness filter that normalizes dialogue to -24 LKFS and limits peak audio to -2 dBFS, guaranteeing that ads never violate federal broadcast loudness standards.""",
    },

    # Q24: Distributed Global Counter & Aggregator for Live Stream Metrics
    {
        "id": 24,
        "title": "Distributed Global Counter and Aggregator for Live Video Concurrent Stream Metrics",
        "category": "Distributed Systems & Telemetry",
        "problem_statement": """Design a distributed, highly available global counter and metric aggregation service for Prime Video live events. The system must accurately track concurrent viewer counts, active stream sessions, and aggregate ad impression velocity across tens of millions of simultaneous viewers globally, updating real-time operations dashboards and ad pacing systems every two seconds with sub-one-percent error.""",
        "clarifying_questions": """To clarify this distributed counting system, I would first ask about the consistency requirements: is an approximate count with bounded error (e.g., within 0.5% of true count) acceptable, or does the system require exact atomic counting across every single viewer connection? For real-time operational monitoring and ad pacing, an approximate count with sub-one-percent error generated using probabilistic algorithms is fully acceptable and vastly more scalable.

Next, I would ask about heartbeat reporting frequency. How often do client video players emit heartbeat pings indicating they are still actively streaming? A standard streaming pattern is for clients to emit a heartbeat ping every thirty or sixty seconds.

I would also clarify the dimensions across which metrics must be aggregated: do we need concurrent stream counts broken down by device type, geographic region, ISP, and video bitrate ladder? Multi-dimensional aggregation requires a scalable roll-up architecture.

Finally, I would ask how the system handles client heartbeat dropouts when viewers abruptly close their apps or lose internet connectivity.""",
        "svg_diagram": generate_svg(
            "Distributed Global Streaming Counter",
            [
                ["Player Heartbeat Pings", "30s Periodic Pings"],
                ["Edge Ingestion Nodes", "Local HyperLogLog Bins"],
                ["Regional Aggregators", "Kafka / Flink Merge"],
                ["Global Metric Store", "Central Redis Cluster"],
                ["Live Operations Wall", "2-Second Metric Refresh"]
            ]
        ),
        "functional_requirements": """Functionally, the service must ingest periodic heartbeat telemetry pings from tens of millions of active Prime Video streaming clients.

It must maintain an accurate count of active concurrent viewers globally, broken down by live broadcast event, sport type, and country.

The system must support multi-dimensional grouping, providing concurrent viewer counts sliced by client device category, video resolution variant, and network carrier.

It must automatically evict inactive viewer sessions if a client fails to emit a heartbeat within an expected timeout window (such as ninety seconds).

Finally, it must publish aggregated concurrent stream metrics every two seconds to real-time operations dashboards, capacity management systems, and ad pacing engines.""",
        "non_functional_requirements": """From a non-functional perspective, metric aggregation and dashboard refresh latency must be under two seconds from the close of each aggregation window.

The system must scale to handle over one million heartbeat pings per second during major live sporting events like Thursday Night Football.

System availability must reach 99.999 percent, ensuring that operations teams never lose visibility into broadcast audience scale.

Counting accuracy must stay within a 0.5 percent error margin compared to ground-truth log reconciliation.""",
        "core_entities": """The primary core entity is the Player Heartbeat Ping, containing the session ID, user ID, broadcast ID, device type, stream bitrate, and client timestamp.

Next is the Regional HyperLogLog Register, storing probabilistic cardinality sketches for active viewers within a specific cloud region.

We also have the Aggregated Stream Metric Record, capturing the timestamp, broadcast ID, total concurrent streams, and dimensional breakdown.

Another entity is the Viewer Session Leaser, tracking the last seen heartbeat timestamp and session expiration deadline for each active stream.

Finally, the Broadcast Audience Summary entity represents the global consolidated audience metrics delivered to executive dashboards and advertiser reporting portals.""",
        "api_design": """The ingestion fleet exposes an ultra-lightweight HTTP/2 endpoint /heartbeat/v1/ping that accepts compressed JSON or binary heartbeat beacons from player SDKs.

The ping endpoint immediately responds with an HTTP 204 No Content status to release client connections instantly.

An internal query API provides real-time metric retrieval for operations dashboards, accepting filters like broadcast_id and dimensions.

A streaming subscription API allows internal services like ad pacing engines to subscribe to real-time viewer count updates via gRPC or Server-Sent Events.""",
        "data_flow": """The data flow begins as millions of Prime Video player applications emit a compact heartbeat beacon every thirty seconds to the nearest edge location.

Edge ingestion proxies validate the beacon and extract the unique viewer session ID and dimension tags.

Instead of writing to a central database, edge proxies insert the session ID into local HyperLogLog data structures maintained in regional Redis clusters.

Every two seconds, regional aggregation workers extract the regional HyperLogLog sketches and publish them to a centralized Kafka topic.

A global aggregation service merges the regional sketches using HyperLogLog union operations, calculates the global concurrent viewer count, and writes the consolidated metrics into an in-memory Redis store for instant dashboard consumption.""",
        "high_level_design": """At a high level, the architecture utilizes a hierarchical distributed aggregation model combining edge ingestion nodes, regional sketch registers, and a centralized union coordinator.

The edge layer comprises an Auto Scaling fleet of Go microservices fronted by AWS Network Load Balancers across multiple global regions.

Regional state management is handled by Amazon ElastiCache for Redis, utilizing Redis HyperLogLog commands (PFADD and PFMERGE) that consume less than one kilobyte of memory per register while providing 0.81 percent standard error.

Data transport between regions utilizes Apache Kafka with MirrorMaker 2 replication for cross-region sketch synchronization.

The global aggregation engine is a lightweight microservice that merges regional sketches every two seconds, updating Amazon Managed Grafana and CloudWatch dashboards in real time.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, maintaining real-time global counts across thirty million concurrent viewers without massive database write contention is achieved through Probabilistic Data Structures. Storing thirty million individual session keys in a traditional database would require gigabytes of RAM and millions of write transactions per second.

By using HyperLogLog registers, our system represents thirty million unique sessions in just twelve kilobytes of memory per dimension slice, allowing millions of unique viewers to be counted using sub-microsecond bitwise operations.

Furthermore, because HyperLogLog sketches are mathematically unionable without loss of precision, regional clusters can merge their local registers independently and transmit tiny twelve-kilobyte sketches to the global aggregator, reducing cross-region network bandwidth by over 99.9 percent.

To handle sudden client dropouts gracefully without artificial lag, the system implements a Sliding Window Decay: heartbeat registrations are divided into three ten-second sub-buckets, and only sessions that have emitted a heartbeat within the last three consecutive buckets are included in the active tally, ensuring instantaneous detection of viewer drop-offs.""",
    },

    # Q25: Secure Multi-Tenant Publisher Ad Server Gateway
    {
        "id": 25,
        "title": "Secure Multi-Tenant Publisher Ad Server Integration Gateway",
        "category": "API Gateway & Partner Integration",
        "problem_statement": """Design a secure, multi-tenant Publisher Ad Server (PAS) integration gateway for Prime Video live events. The system must bridge Prime Video's live broadcast infrastructure with third-party supply-side platforms, external programmatic ad exchanges, and premium sports leagues, enforcing strict tenant isolation, cryptographic payload verification, and rate limiting with sub-fifteen-millisecond latency.""",
        "clarifying_questions": """When clarifying this integration gateway, I would first ask about the protocols and standards supported: does the gateway communicate primarily via OpenRTB standards, proprietary Publisher Ad Server APIs, or customized gRPC channels? Supporting both OpenRTB 2.5/3.0 over HTTP/2 and internal gRPC is standard for modern publisher gateways.

Next, I would ask about tenant isolation requirements. Are third-party partners sharing a multi-tenant compute cluster with logical software isolation, or do high-priority leagues and enterprise partners require dedicated, sandboxed compute resources to prevent noisy neighbor interference? Logical software isolation backed by separate connection pools and CPU quotas is typical.

I would also clarify security and authentication mechanisms: do partner connections use mutual TLS (mTLS) with client certificates, OAuth 2.0 bearer tokens, or HMAC request signatures? Requiring mTLS combined with short-lived HMAC request signatures ensures zero unauthorized access.

Finally, I would ask about payload transformation overhead: how does the gateway translate external partner ad response formats into internal Prime Video manifest schemas without adding latency?""",
        "svg_diagram": generate_svg(
            "Publisher Ad Server Integration Gateway",
            [
                ["External Partner DSP/SSP", "OpenRTB over mTLS"],
                ["Gateway Edge Proxy", "mTLS & HMAC Verify"],
                ["Tenant Sandbox Engine", "Rate Limiting & Quotas"],
                ["Protocol Normalizer", "OpenRTB to Protobuf"],
                ["Prime Video Ad Bus", "Internal Ad Decisioning"]
            ]
        ),
        "functional_requirements": """Functionally, the gateway must terminate secure external connections from third-party advertising partners, supply-side platforms, and sports league systems.

It must authenticate each incoming request using mutual TLS and verify that the partner is authorized to bid on the specific live broadcast property.

The system must enforce strict multi-tenant governance, ensuring that one partner cannot exceed their contracted query-per-second allocation or impact the performance of other partners.

It must parse and validate partner bid responses against industry-standard OpenRTB schemas, sanitizing creative URLs and tracking pixels to prevent malicious script injection.

Finally, it must normalize partner response payloads into internal Protocol Buffer schemas and route them to internal ad decisioning services within fifteen milliseconds.""",
        "non_functional_requirements": """From a non-functional perspective, gateway processing overhead must be under fifteen milliseconds at the P99 percentile, including TLS handshake termination, schema validation, and protocol translation.

The gateway must handle aggregate partner traffic exceeding five hundred thousand requests per second during peak live sports commercial breaks.

Security must be broadcast-grade, with zero possibility of cross-tenant data leakage or unauthorized access to proprietary viewer targeting segments.

System availability must reach 99.999 percent, providing redundant active-active gateway fleets across multiple cloud availability zones.""",
        "core_entities": """The primary core entity is the Partner Tenant Profile, specifying partner ID, authorized league properties, public key certificates, contracted QPS limits, and timeout SLAs.

Next is the Inbound Partner Request, containing the encrypted OpenRTB bid opportunity, tracking cookies, device context, and digital signature.

We also have the Tenant Rate Limit Quota, tracking real-time query consumption, concurrent connection counts, and burst allowances per partner.

Another entity is the Normalized Internal Ad Bid, representing the sanitized, schema-validated bid payload formatted in Protocol Buffers.

Finally, the Gateway Security Audit Log records all authentication failures, malformed payloads, and rate-limit violations for security analysis.""",
        "api_design": """The gateway exposes public-facing HTTPS endpoints adhering to OpenRTB 2.5 and 3.0 specifications, such as POST /v1/openrtb2/auction.

Mutual TLS (mTLS) is enforced at the network edge, requiring partners to present valid X.509 client certificates issued by trusted certificate authorities.

An internal gRPC client forwards normalized bid opportunities to internal ad decisioning services over high-speed virtual private cloud networks.

A tenant administration API allows operations teams to onboard new partners, configure endpoint routing rules, and adjust partner timeout budgets dynamically.""",
        "data_flow": """The data flow begins when an external demand partner sends an OpenRTB bid response over an established mutual TLS connection to our gateway.

The gateway edge proxy validates the partner's client certificate and verifies the cryptographic signature of the request payload.

The tenant governance filter checks whether the partner is within their contracted queries-per-second limit; if exceeded, the request is throttled with an immediate HTTP 429 response.

A high-performance C++ parser validates the OpenRTB JSON payload against strict schema rules, sanitizes creative markup, and translates the data into an internal Protobuf structure.

The normalized bid is dispatched over internal gRPC channels to the live ad decisioning engine, completing the entire gateway processing cycle in under nine milliseconds.""",
        "high_level_design": """At a high level, the architecture consists of an edge security termination tier, a tenant isolation and throttling engine, a protocol translation layer, and internal routing proxies.

The edge security layer utilizes an Auto Scaling fleet of Envoy proxies deployed behind AWS Network Load Balancers, handling hardware-accelerated mTLS termination.

Tenant governance and quota management are powered by high-speed in-memory rate limiting modules integrated directly into Envoy worker threads.

Protocol translation and validation are executed by high-performance Go or C++ microservices running in Kubernetes clusters.

Internal service routing leverages AWS PrivateLink and internal service meshes to deliver normalized bid payloads directly to ad decision workers without traversing the public internet.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, achieving sub-fifteen-millisecond gateway latency while performing complete TLS termination and schema validation requires eliminating expensive handshake overheads. We accomplish this by enforcing Persistent HTTP/2 Connections with TCP keep-alive, allowing partners to reuse pre-authenticated TLS sessions across millions of sequential bid transactions without repeating the cryptographic handshake.

To prevent a rogue or misconfigured partner from causing a Noisy Neighbor outage that degrades other bidders during a live game, the gateway enforces Strict Per-Tenant Connection Isolation: each partner is assigned a dedicated thread pool and socket queue, ensuring that thread exhaustion from one partner cannot impact another.

Security validation of creative markup is performed using high-speed Abstract Syntax Tree sanitizers that strip unsafe JavaScript, iframe tags, and unauthorized tracking pixels, preventing malicious code injection into the Prime Video player SDK.

All gateway instances are stateless and deployed across multiple availability zones in an active-active setup: if an individual gateway node fails, Network Load Balancers reroute partner traffic to healthy instances in sub-millisecond time.""",
    },

    # Q26: Automated Live Broadcast Readiness & Chaos Engineering Platform
    {
        "id": 26,
        "title": "Automated Live Broadcast Readiness and Chaos Engineering Platform",
        "category": "Chaos Engineering & Operational Excellence",
        "problem_statement": """Design an automated live broadcast readiness and chaos engineering platform for Amazon Advertising. The system must run pre-flight operational validation drills, simulated viewer traffic surges (fifteen million virtual viewers), and automated chaos experiments (injecting network latency, killing broker pods, and dropping third-party DSP connections) forty-eight hours before live sporting events to certify broadcast readiness.""",
        "clarifying_questions": """To clarify this chaos engineering platform, I would first ask about the test environment: do chaos drills and pre-flight validation runs execute in an isolated staging environment that mirrors production, or do we run controlled chaos experiments directly in production during dark windows ahead of the live broadcast? Running pre-flight chaos tests in production during dark hours with synthetic traffic provides the only true guarantee of production readiness.

Next, I would ask about safety blast radius controls: how does the system ensure that chaos experiments are immediately aborted if an experiment begins impacting legitimate viewers or live production streams? Automated kill switches tied to real-time production health alarms are mandatory.

I would also clarify the scale of traffic simulation: can the load generation engine simulate realistic client behavior, including video player manifest polling, heartbeat beacons, ad break requests, and random playback dropouts? The load generation must realistically simulate fifteen million concurrent video players.

Finally, I would ask about reporting: does the platform generate an automated Broadcast Readiness Certificate that leadership must sign off on before kickoff?""",
        "svg_diagram": generate_svg(
            "Broadcast Readiness & Chaos Platform",
            [
                ["Pre-Flight Schedule", "48h Before Kickoff"],
                ["Synthetic Traffic Fleet", "15M Simulated Players"],
                ["Chaos Injection Engine", "Latency & Pod Faults"],
                ["Health & Safety Monitor", "Automated Kill Switch"],
                ["Readiness Certification", "Executive Sign-Off"]
            ]
        ),
        "functional_requirements": """Functionally, the platform must allow broadcast reliability engineers to schedule automated pre-flight readiness drills forty-eight hours prior to scheduled live events.

It must deploy a distributed synthetic load generation fleet capable of simulating up to fifteen million concurrent video players polling manifests and firing impression beacons.

The system must execute automated chaos injection scenarios, including simulating cross-region network partitions, dropping ad auction DSP connections, terminating Kafka broker nodes, and injecting Redis latency.

It must continuously monitor core service health metrics during the drill, verifying that automated failover mechanisms, circuit breakers, and fallback slates activate correctly.

Finally, it must generate a structured Broadcast Readiness Scorecard highlighting any architectural weaknesses, SLA breaches, or capacity bottlenecks requiring remediation before the game airs.""",
        "non_functional_requirements": """From a non-functional perspective, safety is paramount: the platform must feature an instantaneous automated Kill Switch that aborts all chaos injections within five hundred milliseconds if any production health threshold is breached.

The synthetic load generator must scale elastically across thousands of cloud instances to generate millions of requests per second without becoming a bottleneck itself.

Test repeatability is essential, ensuring that identical chaos drill scenarios can be executed consistently before every Thursday Night Football and NBA broadcast throughout the season.

The platform must maintain comprehensive audit logging, recording all injected failure parameters, system responses, and recovery timelines for compliance review.""",
        "core_entities": """The primary core entity is the Broadcast Readiness Drill, tracking the target sporting event, scheduled drill window, participating microservices, and overall pass/fail status.

Next is the Chaos Experiment Specification, defining the fault injection type, target service, duration, latency injection values, and expected failover behavior.

We also have the Synthetic Viewer Scenario, defining playback behaviors, manifest polling frequencies, ad interaction patterns, and device distribution ratios.

Another entity is the Automated Safety Policy, capturing the critical health metric thresholds that trigger an immediate emergency experiment abort.

Finally, the Broadcast Readiness Scorecard entity encapsulates test results, latency percentiles under failure, failover recovery times, and certified capacity headroom.""",
        "api_design": """The platform provides an orchestration REST API /readiness/v1/drills allowing engineers to trigger, monitor, and abort pre-flight validation runs.

There is a chaos injection API used by agent controllers to command chaos agents running inside Kubernetes clusters and AWS infrastructure.

A synthetic traffic control API allows test orchestrators to dynamically ramp traffic from zero to fifteen million simulated viewers following realistic viewership curves.

A reporting API exports structured markdown and PDF readiness certificates to Slack channels and internal broadcast operational wiki pages.""",
        "data_flow": """The data flow begins forty-eight hours before kickoff when the readiness platform initiates an automated pre-flight certification drill during an off-peak broadcast window.

The orchestrator spins up an Auto Scaling fleet of synthetic player agents across multiple AWS regions, ramping synthetic viewer traffic to fifteen million simulated streams.

Simultaneously, the chaos injection engine commands AWS Fault Injection Service and Kubernetes chaos daemons to inject thirty milliseconds of artificial network latency into the primary ad decisioning cluster.

The platform monitors edge SSAI proxies, observing that the circuit breaker trips within fifty milliseconds and successfully diverts manifest requests to secondary regional clusters without dropped requests.

Upon completing all planned failure scenarios, the platform winds down synthetic traffic, removes all chaos injections, compiles metric logs, and publishes a certified readiness report to the engineering lead.""",
        "high_level_design": """At a high level, the architecture combines a centralized drill orchestrator, a distributed synthetic load generation engine, a multi-layer chaos injection framework, and an automated safety monitoring system.

The drill orchestrator is built with Python and Temporal workflows, coordinating long-running multi-stage validation drills with deterministic state tracking.

Synthetic traffic generation is powered by distributed Locust or custom Go load generators running across thousands of AWS Fargate tasks.

Chaos injection is managed through integration with AWS Fault Injection Service (FIS) and Chaos Mesh deployed within production Amazon EKS clusters.

Safety monitoring is anchored by an independent Prometheus and CloudWatch agent that continuously queries live operational metrics, maintaining a direct hardware-level abort connection to all chaos daemons.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, ensuring absolute safety during chaos drills in production environments requires multi-tiered safety blast radius controls. The platform implements an Automated Emergency Abort Controller: an independent monitor checks production error rates every second, and if errors rise above 0.1 percent, it immediately triggers an emergency abort, rolling back all injected faults and resetting routing rules in under five hundred milliseconds.

To ensure realistic traffic simulation during drills, synthetic player agents do not simply generate repetitive HTTP requests; they execute full stateful video player simulations, including HLS manifest sequence tracking, bitrate switching based on simulated network jitter, and realistic beacon timing.

Chaos drills evaluate both technical failover and operational human readiness: the platform automatically triggers real PagerDuty alarms to test on-call engineer response times and verifies that automated runbook assistants correctly diagnose injected faults.

A broadcast event is only certified for air once the system demonstrates that every single failure scenario—from a total loss of a cloud availability zone to the failure of top external DSPs—recovers automatically without a single viewer observing a frozen video stream.""",
    },

    # Q27: Privacy-Preserving Clean Room Infrastructure for Live Sports
    {
        "id": 27,
        "title": "Privacy-Preserving Clean Room Infrastructure for Live Sports Advertisers",
        "category": "Data Privacy & Clean Rooms",
        "problem_statement": """Design a privacy-preserving data clean room infrastructure for Amazon Advertising in live sports. The system must allow major brand advertisers (such as automotive and consumer goods companies) to run joint measurement, attribution, and audience overlap queries against Amazon's live sports viewership data without exposing raw Personally Identifiable Information (PII) or proprietary customer records to either party.""",
        "clarifying_questions": """When clarifying this clean room architecture, I would first ask about the computational privacy techniques required: are we relying on cryptographic secure multi-party computation (SMPC), differential privacy with mathematical noise injection, or hardware-enforced trusted execution environments (like AWS Nitro Enclaves)? A combination of AWS Clean Rooms with Nitro Enclaves and differential privacy is the industry standard for enterprise advertising.

Next, I would ask about the supported query types: do advertisers need to run arbitrary SQL queries, or are queries restricted to pre-approved measurement templates such as reach and frequency analysis, multi-touch attribution, and audience overlap intersection? Restricting clean room operations to vetted analytical query templates prevents data exfiltration attacks.

I would also clarify the scale of datasets: how many millions of viewer records and advertiser transaction rows are joined during a typical clean room query? Datasets often span hundreds of millions of records, requiring distributed analytical processing.

Finally, I would ask about query execution latency: while real-time ad serving requires milliseconds, clean room analytical queries typically run in batch mode with acceptable turnaround times of minutes to hours.""",
        "svg_diagram": generate_svg(
            "Privacy-Preserving Data Clean Room",
            [
                ["Advertiser CRM Data", "Hashed Customer Records"],
                ["Amazon Sports Data", "Verified Viewer Sessions"],
                ["AWS Nitro Enclave", "Isolated Hardware Sandbox"],
                ["Differential Privacy", "Mathematical Noise Guard"],
                ["Attribution Report", "Privacy-Safe Aggregates"]
            ]
        ),
        "functional_requirements": """Functionally, the clean room must allow enterprise advertisers to securely upload anonymized customer datasets, including purchase histories and CRM records.

It must ingest Amazon's live sports viewership logs, including ad impressions delivered during events like Thursday Night Football.

The system must perform privacy-safe cryptographic matching across datasets using pseudonymized identifiers like hashed emails or unified ID tokens.

It must execute joint analytical computations inside an isolated sandbox, evaluating campaign reach, incremental sales lift, and multi-touch attribution models.

Finally, it must apply differential privacy algorithms to query outputs, ensuring that all published reports contain only aggregate statistics and mathematically prevent the reconstruction of individual user data.""",
        "non_functional_requirements": """From a non-functional perspective, data security is the paramount requirement: zero cleartext PII or raw customer identifiers can ever be visible to Amazon employees or the external advertiser.

The system must scale to join and analyze datasets containing hundreds of millions of rows within fifteen minutes for a standard measurement query.

Regulatory compliance must satisfy global privacy frameworks including GDPR, CCPA, and COPPA, with full cryptographic audit logging of all executed queries.

System availability must be 99.9 percent, providing reliable analytical reporting portals for enterprise marketing teams.""",
        "core_entities": """The primary core entity is the Clean Room Collaboration, defining the participating advertiser, approved live sports campaigns, allowed query templates, and data governance policies.

Next is the Anonymized Advertiser Dataset, containing one-way salted hashes of customer identifiers and associated offline transaction records.

We also have the Live Event Viewership Ledger, representing verified ad impression logs linked to anonymized viewer tokens.

Another entity is the Analytical Query Specification, defining the SQL computation template, aggregation metrics, group-by dimensions, and privacy budget limits.

Finally, the Aggregated Attribution Report captures the resulting incremental lift percentages, matched audience sizes, and statistical confidence intervals.""",
        "api_design": """The clean room platform provides an authenticated REST API /cleanroom/v1/collaborations for configuring clean room partnerships and linking data tables.

An analytical query submission API /cleanroom/v1/queries allows authorized data scientists to submit measurement jobs against approved templates.

There is a data ingestion API supporting encrypted batch uploads directly to dedicated Amazon S3 buckets protected with customer-managed KMS keys.

A reporting API allows advertiser business intelligence tools to download finalized, privacy-vetted analytical summaries and lift graphs.""",
        "data_flow": """The data flow begins when an advertiser uploads an encrypted dataset of recent car purchases to their dedicated Amazon S3 bucket, using a customer-managed KMS key.

Amazon Advertising writes verified live sports ad impression logs to an isolated S3 storage bucket.

The clean room orchestrator launches a distributed computing job inside an AWS Nitro Enclave, a hardware-isolated compute sandbox with no external network access or interactive shell.

The enclave loads both datasets into memory, decrypts them using ephemeral keys negotiated via cryptographic attestation, and performs a private join on hashed identifiers.

The analytical aggregation is computed, mathematical noise is injected via a differential privacy algorithm to satisfy the privacy budget, and the final aggregate report is exported to the advertiser portal.""",
        "high_level_design": """At a high level, the architecture leverages AWS Clean Rooms, AWS Nitro Enclaves, and Apache Spark running in isolated Amazon EMR clusters.

Data storage is strictly segregated: advertiser data and Amazon viewership data reside in separate, dedicated S3 buckets with independent KMS encryption keys.

Compute isolation is enforced by AWS Nitro Enclaves, ensuring that memory contents cannot be accessed even by users with root administrative privileges on the host system.

Differential privacy enforcement is handled by an automated privacy layer that tracks cumulative privacy loss (epsilon budget) across queries and automatically rejects queries that could compromise anonymity.

An immutable audit ledger built on Amazon QLDB or cryptographically signed logs records every query template, input hash, and execution timestamp for legal compliance.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, guaranteeing mathematical privacy against linkage and reconstruction attacks requires rigorous Differential Privacy and Query Template Whitelisting. The clean room strictly prohibits arbitrary SQL queries like SELECT * FROM users; instead, advertisers can only execute pre-approved parameterized templates that enforce minimum aggregation thresholds (e.g., any cohort smaller than one hundred individuals is automatically suppressed).

To protect against differential reconstruction attacks (where an attacker submits multiple overlapping queries to isolate a single individual's behavior), the system enforces a strict Epsilon Privacy Budget: each executed query consumes a portion of the collaboration's privacy budget, and once the budget is exhausted, no further queries can be executed on that dataset.

Hardware-level isolation via AWS Nitro Enclaves provides cryptographic attestation: before any data is decrypted, the KMS key policy verifies the SHA-384 measurement hash of the enclave's running code, ensuring that not a single line of unvetted software can run inside the environment.

This architecture provides mathematically provable privacy guarantees, enabling Fortune 500 advertisers to measure multi-million-dollar live sports advertising campaigns with complete confidence in regulatory compliance.""",
    },

    # Q28: Dynamic Bitrate (ABR) Ad Transcoding & Audio Normalization Pipeline
    {
        "id": 28,
        "title": "Intelligent Dynamic Bitrate Ad Transcoding and Audio Normalization Pipeline",
        "category": "Video Engineering & Transcoding",
        "problem_statement": """Design an intelligent, automated video transcoding and audio normalization pipeline for Prime Video advertising. The system must ingest raw advertiser commercial video submissions, automatically transcode them into dozens of Adaptive Bitrate (ABR) profiles matching live broadcast video ladders, normalize audio loudness to -24 LKFS broadcast standards, and package segments in under ten minutes with zero visual artifacts.""",
        "clarifying_questions": """To properly scope this transcoding pipeline, I would first ask about the input and output video formats: what codecs and containers do advertisers submit, and what streaming packaging formats are required? Advertisers typically submit high-bitrate ProRes or H.264 MP4 files, and the pipeline must transcode them into H.264 (AVC), H.265 (HEVC), and AV1 formats packaged into fragmented MP4 (fMP4) for both HLS and DASH streaming.

Next, I would ask about segment alignment: why is segment alignment so critical in live ad insertion? In live SSAI, ad video segments must match the exact duration (e.g., exactly two seconds), GOP (Group of Pictures) size, and keyframe intervals of the surrounding live football broadcast; any mismatch causes client video players to stutter or lose audio sync.

I would also clarify the turnaround SLA: how quickly must a newly uploaded ad creative be validated, transcoded, and certified for broadcast? A turnaround time of under ten minutes enables rapid advertiser turnaround during live tournament broadcasts.

Finally, I would ask about automated quality control: the system must automatically inspect transcoded video for dropped frames, blockiness, color banding, and audio clipping.""",
        "svg_diagram": generate_svg(
            "ABR Ad Transcoding & Audio Normalization",
            [
                ["Advertiser Creative Upload", "ProRes / H.264 Master"],
                ["Audio Normalizer", "ITU BS.1770 -24 LKFS"],
                ["Distributed Transcoder", "AWS Elemental / FFmpeg"],
                ["Automated Video QC", "VMAF & Segment Alignment"],
                ["CDN Edge Distribution", "Broadcast-Ready ABR"]
            ]
        ),
        "functional_requirements": """Functionally, the platform must accept master video commercial uploads from advertisers and automated campaign management systems via secure S3 upload portals.

It must inspect the source file to verify resolution, framerate, color space, and audio channel configurations, rejecting corrupted or non-compliant source files immediately.

The system must normalize the audio track to strict broadcast standards (-24 LKFS loudness target and -2 dBFS true peak limit) to ensure commercial breaks do not play louder than the surrounding sports game.

It must transcode the video into a complete Adaptive Bitrate (ABR) ladder spanning resolutions from 360p up to 4K HDR across multiple codecs including H.264, HEVC, and AV1.

Finally, it must segment the transcoded streams into frame-accurate, aligned video chunks with closed captions, generating HLS and DASH manifests and publishing assets to global CDN origins in under ten minutes.""",
        "non_functional_requirements": """From a non-functional perspective, end-to-end processing time for a thirty-second commercial must not exceed ten minutes from upload completion to global CDN availability.

Transcoded video quality must achieve a Video Multi-Method Assessment Fusion (VMAF) score of at least ninety-three across all bitrate tiers, guaranteeing pristine broadcast visual fidelity.

GOP and segment boundary alignment must be 100 percent deterministic, ensuring that ad segments splice seamlessly into live broadcast streams with zero playback buffering.

The transcoding cluster must scale elastically to handle sudden surges of hundreds of commercial creative submissions ahead of major sporting event kickoffs.""",
        "core_entities": """The primary core entity is the Creative Transcoding Job, tracking the master asset ID, submission timestamp, priority level, target ABR profile, and processing pipeline state.

Next is the Source Media Inspection Profile, recording the source codec, container, framerate, aspect ratio, audio channels, and measured input loudness.

We also have the ABR Ladder Specification, defining the target resolutions, bitrates, frame rates, codec profiles, and segment durations for each streaming tier.

Another entity is the Quality Control (QC) Report, capturing the automated VMAF scores, audio peak levels, dropped frame counts, and compliance certifications.

Finally, the Broadcast-Ready Creative Package entity maps all generated video chunks, audio segments, closed caption tracks, and CDN origin URLs.""",
        "api_design": """The service provides an asynchronous creative submission API /transcode/v1/jobs where advertisers upload video files and initiate transcoding workflows.

There is a job status query API /transcode/v1/jobs/{job_id} that provides real-time progress percentages, intermediate QC metrics, and error logs.

A webhook notification service dispatches automated completion events to the ad server creative repository when assets are certified for broadcast.

An administrative API allows broadcast video engineers to update ABR ladder configurations, adjust VMAF quality thresholds, and inspect failed transcoding logs.""",
        "data_flow": """The data flow begins when an advertiser uploads a master commercial file to an Amazon S3 drop bucket, triggering an S3 ObjectCreated event.

The event triggers an AWS Step Functions workflow that spins up a validation worker to inspect the container and codec headers using FFprobe.

The audio track is extracted and passed through an automated audio normalization worker that applies an ITU-R BS.1770 filter to adjust loudness to exactly -24 LKFS.

The normalized audio and video master are dispatched to a distributed transcoding cluster powered by AWS Elemental MediaConvert or containerized FFmpeg workers on EKS.

The cluster transcodes the video into all target ABR variants simultaneously, packages segments into two-second aligned fMP4 chunks, computes VMAF quality scores, and replicates finalized files across global S3 origin buckets in under eight minutes.""",
        "high_level_design": """At a high level, the architecture is designed as an event-driven, distributed media processing pipeline orchestrated by AWS Step Functions and AWS Batch.

Storage is anchored by Amazon S3, utilizing S3 Intelligent-Tiering and multi-region replication to distribute finalized media chunks to CDN origins worldwide.

Transcoding compute is managed by an Auto Scaling cluster of GPU-accelerated EC2 instances (utilizing NVIDIA NVENC hardware encoders) managed by Kubernetes and AWS Batch.

Audio normalization and quality control checks are performed by lightweight C++ workers leveraging libavfilter and libvmaf libraries.

The creative catalog and job tracking state are maintained in Amazon Aurora PostgreSQL, integrated with Amazon CloudWatch for end-to-end pipeline observability.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, achieving seamless live video splicing during Thursday Night Football requires strict Segment Boundary and GOP Alignment. If a live football broadcast utilizes two-second segments with a sixty-frame Group of Pictures (GOP) closed at every keyframe, any stitched ad segment must mirror this exact GOP cadence; even a single missing frame or open GOP boundary causes video player decoders to stutter or crash.

Our transcoding engine enforces Closed GOP encoding with fixed IDR keyframe intervals placed at exact two-second timestamps, guaranteeing that ad segments can be spliced into live playlists without any video decoder reinitialization.

Audio compliance with the Commercial Advertisement Loudness Mitigation (CALM) Act is guaranteed through a two-pass loudness normalization algorithm: the first pass measures integrated loudness across the entire commercial, and the second pass applies linear gain adjustments to hit -24 LKFS with a hard limiter at -2 dBFS, eliminating jarring volume jumps when transitioning between the game and commercial breaks.

Automated Visual Quality Control is enforced by computing VMAF scores against the master asset: if any transcoded rendition scores below ninety-two, the pipeline automatically flags the asset for human review and boosts encoding bitrate, ensuring viewers never see pixelation or macroblocking during live sports broadcasts.""",
    },

    # Q29: Real-Time Chat Sentiment & Contextual Ad Insertion
    {
        "id": 29,
        "title": "Real-Time Chat Sentiment and Contextual Ad Insertion for Interactive Streams",
        "category": "NLP & Interactive Live Streaming",
        "problem_statement": """Design a real-time chat sentiment analysis and contextual ad insertion engine for Prime Video interactive live sports streams. The system must ingest over one million live fan chat messages per minute, analyze crowd sentiment and trending player topics using streaming NLP models, and dynamically select contextual sponsor advertisements within three seconds of a viral fan reaction.""",
        "clarifying_questions": """When clarifying this chat analysis and advertising system, I would first ask about chat volume and velocity: during dramatic game moments (such as a game-winning goal), chat velocity can spike from tens of thousands to over one million messages per minute; how do we handle this ingestion surge without dropping messages? The chat ingestion pipeline must be decoupled from the NLP analysis tier using partitioned streaming buffers.

Next, I would ask about the nature of sentiment analysis: are we classifying broad emotional valence (positive celebration versus negative disappointment), or are we extracting specific named entities like player names, team hashtags, and product mentions? Named Entity Recognition (NER) combined with sentiment classification is essential to link viewer reactions to specific commercial sponsors.

I would also clarify the advertising output: does the system trigger interactive in-chat sponsor banners, on-screen graphical overlays, or prioritize upcoming video ad pods? In-chat sponsored cards and synchronized on-screen lower-third overlays are the primary monetization channels.

Finally, I would ask about content moderation: the system must strictly filter profanity, toxic comments, and harassment before aggregating sentiment signals.""",
        "svg_diagram": generate_svg(
            "Real-Time Chat Sentiment & Contextual Ad Engine",
            [
                ["Live Fan Chat Stream", "1M Messages / Min"],
                ["Profanity & Toxicity Filter", "Sub-10ms Fast Gate"],
                ["Streaming NLP Model", "Sentiment & Entity Extractor"],
                ["Trending Topic Aggregator", "Flink 5-Second Window"],
                ["Contextual Sponsor Card", "Sub-3s Interactive Ad"]
            ]
        ),
        "functional_requirements": """Functionally, the engine must ingest live fan chat messages emitted by viewers participating in interactive Prime Video live event streams.

It must filter incoming messages through an automated profanity and toxicity detection filter, discarding inappropriate content from public display and sentiment aggregation.

The system must evaluate sanitized messages using streaming Natural Language Processing (NLP) models to extract emotional sentiment, trending player names, and key game themes.

It must aggregate sentiment metrics across rolling five-second sliding windows, identifying viral fan spikes such as overwhelming excitement for a specific player's performance.

Finally, it must trigger contextual sponsor messages (such as an energy drink sponsor celebrating high energy moments) in the live chat feed and display synchronized graphical overlays within three seconds of the spike.""",
        "non_functional_requirements": """From a non-functional perspective, end-to-end processing latency from a viral chat surge to contextual ad placement must be under three seconds to capitalize on real-time viewer excitement.

The chat ingestion and analysis pipeline must comfortably scale to handle over one million messages per minute during peak live sports moments.

Sentiment classification accuracy must exceed eighty-five percent across informal sports slang, emojis, and multilingual text expressions.

System availability must reach 99.99 percent, ensuring that chat monetization features remain active throughout the live broadcast.""",
        "core_entities": """The primary core entity is the Raw Chat Message, containing the user ID, broadcast ID, message text, client timestamp, and emoji reactions.

Next is the Sanitized Chat Token, representing the profanity-filtered message text tagged with language codes.

We also have the Extracted Sentiment Feature, capturing the positive, negative, or neutral sentiment scores and identified sports entities.

Another entity is the Trending Topic Aggregate, tracking message frequency, sentiment polarity, and velocity for specific player and team keywords over rolling five-second windows.

Finally, the Contextual Chat Sponsor Campaign entity defines the sponsor creative, trigger keywords, minimum sentiment threshold, and pacing limits.""",
        "api_design": """The chat platform exposes an active WebSocket endpoint /chat/v1/stream used by client video players to send and receive real-time fan comments.

An internal gRPC query API /sentiment/v1/current-trend allows advertising engines to fetch active sentiment scores and trending topic tags on demand.

There is a campaign configuration REST API where advertisers can sponsor specific game triggers (such as high excitement or team celebrations) and configure in-chat sponsor cards.

A real-time telemetry streaming API emits chat sentiment indices, message volume graphs, and ad engagement metrics to broadcast operations dashboards.""",
        "data_flow": """The data flow begins as viewers type comments and react with emojis in the Prime Video interactive chat interface during a live game.

The messages are received by an AWS AppSync or WebSocket API gateway fleet that streams raw text into an Apache Kafka topic.

A lightweight toxicity filter purges offensive language, forwarding sanitized text to an Apache Flink streaming application.

Flink dispatches message batches to an optimized NLP model running on GPU clusters, extracting entity mentions and sentiment scores in under twenty milliseconds.

Flink aggregates the scores across five-second tumbling windows; when excitement for a star player spikes past a configured threshold, the engine matches the event with an active sponsor campaign and broadcasts an interactive sponsor card into the live chat feed in under two seconds.""",
        "high_level_design": """At a high level, the architecture is split into a real-time messaging gateway, an automated moderation tier, a streaming NLP processing pipeline, and a contextual ad delivery system.

The messaging gateway utilizes AWS AppSync and Amazon API Gateway to maintain millions of concurrent persistent WebSocket connections with client devices.

Message buffering is handled by high-throughput Apache Kafka clusters partitioned by live broadcast fixture IDs.

Streaming NLP and aggregation are powered by Apache Flink and lightweight DistilBERT or RoBERTa models optimized with ONNX Runtime running on GPU-accelerated Kubernetes nodes.

Contextual ad dispatching is managed by a microservice that injects sponsored interactive cards directly into the WebSocket broadcast channels delivered to viewers' chat windows.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, processing one million informal chat messages per minute with deep NLP models without incurring prohibitive GPU compute costs requires a Two-Tier Cascaded Processing Architecture. Running a full transformer model on every single chat message is computationally wasteful because sports chat contains repetitive phrases and single-emoji messages (like fire or clapping emojis).

Our pipeline applies a High-Speed Lexical & Emoji Filter as the first tier: messages consisting purely of standard emojis or basic excitement phrases are scored instantaneously using an in-memory dictionary taking microseconds on CPU.

Only rich, multi-word textual sentences are routed to the second-tier GPU transformer model, reducing deep learning inference load by over seventy percent while maintaining high sentiment precision.

To guarantee that sponsored chat cards are not spammed during continuous excitement, the contextual ad engine enforces an in-chat Frequency Cooldown: once a sponsor message is triggered, an automated five-minute cooldown is applied to that sponsor tier, preserving viewer engagement and chat authenticity.""",
    },

    # Q30: Multi-Agent Broadcast Operations Control Plane for Live Events
    {
        "id": 30,
        "title": "Multi-Agent Broadcast Operations Control Plane for Live Event Command Center",
        "category": "Multi-Agent Systems & Operational Control",
        "problem_statement": """Design a multi-agent AI broadcast operations control plane for the Prime Video Live Event Command Center. The system must coordinate specialized AI agents (including an Ingest Monitor Agent, an SSAI Manifest Agent, an Ad Auction Agent, and an Incident Commander Agent) to autonomously monitor, diagnose, and manage advertising infrastructure across fifty concurrent live sporting events worldwide.""",
        "clarifying_questions": """When clarifying this multi-agent control plane, I would first ask about the agent coordination model: do the agents operate in a hierarchical structure where a supervisor Incident Commander agent delegates tasks to specialized domain agents, or do they operate as a peer-to-peer decentralized mesh? A hierarchical supervisor model provides clear escalation paths, deterministic decision-making, and superior auditability during high-stakes live sports broadcasts.

Next, I would ask how agents communicate: do they share a centralized state blackboard, exchange structured JSON messages over an event bus, or use the Model Context Protocol (MCP)? Combining Model Context Protocol for tool execution with an event-driven shared blackboard architecture allows agents to inspect shared broadcast context seamlessly.

I would also clarify the human-in-the-loop governance: what level of human oversight is required for critical operational interventions? Broadcast directors must retain veto authority over high-impact actions through a real-time command dashboard.

Finally, I would ask about scalability: the control plane must supervise fifty concurrent live sporting events across multiple sports, time zones, and global regions without cross-event interference.""",
        "svg_diagram": generate_svg(
            "Multi-Agent Broadcast Control Plane",
            [
                ["Live Telemetry Streams", "50 Concurrent Events"],
                ["Specialized Domain Agents", "Ingest, SSAI, Auction"],
                ["Supervisor Commander Agent", "Hierarchical Planner"],
                ["MCP Shared Tool Bus", "Safe Operational Actions"],
                ["Operations Command Wall", "Human-in-the-Loop Veto"]
            ]
        ),
        "functional_requirements": """Functionally, the control plane must orchestrate multiple specialized AI agents, each dedicated to monitoring a specific domain of the live advertising stack.

The Ingest Agent must monitor video transport stream integrity, SCTE-35 ad break cue points, and encoder synchronization across all broadcast feeds.

The SSAI Manifest Agent must oversee manifest generation latencies, segment stitching error rates, and CDN edge cache hit ratios.

The Auction Agent must monitor DSP response latencies, bid participation rates, clearing price distributions, and budget pacing health.

The Supervisor Incident Commander Agent must correlate findings across domain agents, synthesize unified situational awareness, formulate holistic remediation plans, and present interactive recommendations to human broadcast directors.""",
        "non_functional_requirements": """From a non-functional perspective, inter-agent communication and diagnostic reasoning must execute within fifteen seconds to provide immediate situational awareness during live broadcast anomalies.

The multi-agent infrastructure must maintain 99.999 percent operational availability, operating independently of the underlying streaming and ad serving data path.

System actions must be completely deterministic and auditable, maintaining immutable logs of all agent reasoning steps, cross-agent messages, and tool invocations.

The control plane must scale to supervise fifty concurrent live sporting events simultaneously without performance degradation or state cross-talk.""",
        "core_entities": """The primary core entity is the Broadcast Event State Blackboard, maintaining the live operational state, active agent assignments, and metric summaries for each live game.

Next is the Specialized Agent Profile, defining the agent's role, subscribed telemetry topics, permitted MCP tools, and operational boundaries.

We also have the Inter-Agent Message Entity, capturing structured communications between domain agents and the supervisor commander.

Another entity is the Multi-Agent Incident Assessment, consolidating diagnosed root causes, confidence scores, and multi-domain impact analyses.

Finally, the Coordinated Remediation Plan entity defines the ordered sequence of operational actions, required safety checks, and human sign-off statuses.""",
        "api_design": """The control plane exposes an internal gRPC and WebSocket API /agents/v1/control-bus that facilitates structured message exchange between agents and the central blackboard.

An interactive Command Center REST and WebSocket API powers the broadcast operations room video wall, streaming live agent dialogue and diagnostic visualizations.

There is an MCP Gateway API that exposes standardized, sandboxed operational tools to agents using Model Context Protocol specifications.

A governance API allows human broadcast commanders to pause agent autonomy, approve pending remediation plans, or issue direct overriding instructions.""",
        "data_flow": """The data flow begins as real-time telemetry from live broadcasts streams into the central event bus across all fifty active sporting events.

The SSAI Manifest Agent detects that manifest generation latency has spiked to seventy milliseconds in a specific European region.

The SSAI Agent posts a structured alert to the shared blackboard, requesting correlation from other domain agents.

The Auction Agent inspects its domain and reports that an external European DSP is timing out on bids, causing worker thread queuing in the manifest layer.

The Supervisor Incident Commander Agent synthesizes both reports, formulates a remediation plan to trip the circuit breaker for that DSP, and presents the plan on the Command Center video wall, where the human director clicks Approve to execute the fix in five seconds.""",
        "high_level_design": """At a high level, the architecture combines an event-driven telemetry distribution tier, a multi-agent orchestration core, a Model Context Protocol tool execution mesh, and an interactive human oversight portal.

Telemetry distribution is managed by Apache Kafka, streaming high-frequency metrics into domain-specific consumer groups.

The multi-agent orchestration core is implemented with Python, LangGraph, and Amazon Bedrock, utilizing stateful graph workflows to coordinate agent reasoning cycles.

Agent tool execution is mediated through an MCP Gateway that enforces strict role-based access control, parameter validation, and audit logging on every infrastructure command.

The human interface is delivered via a modern Next.js and React operations dashboard integrated with WebSockets for real-time video wall updates and one-click incident approvals.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, coordinating multiple autonomous AI agents during high-stakes live sports broadcasts without communication deadlocks or hallucinated actions requires strict Multi-Agent Governance Protocols. We organize agents in a Strict Hierarchical Tree: domain agents (Ingest, SSAI, Auction) are strictly read-only diagnostic workers that analyze telemetry and propose hypotheses; they are physically prohibited from executing infrastructure modifications directly.

Only the centralized Supervisor Incident Commander Agent has the authority to assemble a remediation plan, which must pass through an automated Deterministic Policy Engine that verifies action safety against pre-approved runbooks before presenting it to human engineers.

To prevent agent dialogue loops and token explosion during complex incidents, all inter-agent messages use compact, schema-validated JSON structures rather than freeform text, and multi-agent reasoning cycles are bounded by a hard three-turn limit.

Every agent thought trace, cross-agent message, and human approval is cryptographically signed and stored in Amazon S3 with immutable WORM retention, providing an audit trail for post-broadcast reviews and regulatory compliance."""
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(sysde_questions_part3)} System Design questions (Part 3).")
