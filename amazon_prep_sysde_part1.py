# -*- coding: utf-8 -*-
"""
Amazon Advertising in Live Events - AI Engineer Preparation
Part 2A: System Design Questions 1 to 10
All sections written in small, conversational paragraph chunks without ANY bullet points.
Candidate: Ashutosh Rudraksh
"""

def generate_svg(title: str, steps: list) -> str:
    boxes = ""
    arrows = ""
    x_start = 40
    y = 60
    box_w = 170
    box_h = 75
    spacing = 40
    
    for i, step in enumerate(steps):
        x = x_start + i * (box_w + spacing)
        boxes += f'''
        <g class="node">
          <rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="10" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
          <text x="{x + box_w//2}" y="{y + 28}" text-anchor="middle" fill="#f8fafc" font-size="12" font-weight="bold" font-family="system-ui">{step[0]}</text>
          <text x="{x + box_w//2}" y="{y + 48}" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="system-ui">{step[1]}</text>
        </g>'''
        if i < len(steps) - 1:
            arrow_x = x + box_w
            arrow_end = arrow_x + spacing
            arrows += f'''
            <g class="arrow">
              <line x1="{arrow_x}" y1="{y + box_h//2}" x2="{arrow_end - 6}" y2="{y + box_h//2}" stroke="#f59e0b" stroke-width="2" stroke-dasharray="4"/>
              <polygon points="{arrow_end},{y + box_h//2} {arrow_end - 8},{y + box_h//2 - 5} {arrow_end - 8},{y + box_h//2 + 5}" fill="#f59e0b"/>
            </g>'''
            
    total_w = x_start * 2 + len(steps) * box_w + (len(steps) - 1) * spacing
    return f'''<div class="sys-diagram-container" style="overflow-x:auto; margin: 18px 0; background: #0f172a; border-radius: 12px; padding: 16px; border: 1px solid #334155;">
      <svg width="{max(total_w, 880)}" height="170" viewBox="0 0 {max(total_w, 880)} 170" xmlns="http://www.w3.org/2000/svg">
        <text x="24" y="32" fill="#38bdf8" font-size="15" font-weight="bold" font-family="system-ui">{title}</text>
        {boxes}
        {arrows}
      </svg>
    </div>'''

sysde_questions_part1 = [
    # Q1: SSAI for Thursday Night Football
    {
        "id": 1,
        "title": "Server-Side Dynamic Ad Insertion (SSAI) Engine for Thursday Night Football",
        "category": "Live Video Streaming & Ad Insertion",
        "problem_statement": """Design a broadcast-grade Server-Side Ad Insertion (SSAI) platform for Thursday Night Football on Prime Video. The system must seamlessly stitch targeted video advertisements into the live HLS and DASH video manifests for over 15 million concurrent viewers when an upstream SCTE-35 cue point signal announces a commercial break, without causing playback buffering or stream desynchronization.""",
        "clarifying_questions": """When approaching this problem, the first thing I would clarify with the interviewer is the scale of concurrent viewers and how sudden the spikes are. For Thursday Night Football, we have roughly fifteen million concurrent viewers, and every viewer enters the commercial break at the exact same second when a commercial cue is triggered.

Next, I would ask about latency and manifest delivery protocol constraints. We need to know whether the stream is formatted in HLS or DASH, what the typical chunk segment duration is, and what our end-to-end manifest generation budget looks like. Usually, live low-latency video chunks are two seconds long, meaning manifest generation cannot take more than fifty milliseconds.

Finally, I would ask about fallback behavior and advertiser compliance. If the real-time ad selection system fails or takes too long, we need to know whether we should fall back to a default house ad or a branded stream slate, and whether we need to stitch audio and video segments that exactly match the viewer's current resolution and bitrate ladder without any audio pops or video stutter.""",
        "svg_diagram": generate_svg(
            "Thursday Night Football SSAI Architecture",
            [
                ["Live Video Ingest", "SCTE-35 Cue Markers"],
                ["SSAI Manifest Engine", "Per-User Stitcher"],
                ["Ad Decision Server", "RTB & Target Rules"],
                ["ABR Video Transcoder", "Segment Matcher"],
                ["CloudFront Edge CDN", "Manifest Delivery"]
            ]
        ),
        "functional_requirements": """From a functional perspective, the system must detect upstream broadcast SCTE-35 markers embedded in the live transport stream that signal the start and duration of an impending commercial break.

Once that marker is detected, the platform must query our ad decision engine to select a personalized sequence of video advertisements tailored to each viewer's profile, geographic location, and device capabilities.

The service must then stitch the media URLs for those chosen ads directly into each viewer's live HLS master and media playlists, ensuring the video segments perfectly match the viewer's active adaptive bitrate resolution profile.

Lastly, the system needs to emit server-side impression beacons to third-party measurement and tracking partners as the viewer progresses through playback, confirming each ad was delivered and viewed.""",
        "non_functional_requirements": """On the non-functional side, ultra-low latency is paramount because live video manifests must be generated and delivered within fifty milliseconds to prevent the viewer's playback buffer from running dry and causing video stalling.

The system must handle enormous peak concurrency, scaling up to support fifteen million simultaneous stream requests hitting the manifest generation layer in unison when the referee calls a timeout.

Reliability must be at least four nines because any failure during a high-stakes football broadcast directly leads to lost advertising revenue and poor viewer experience.

Security and anti-tampering are also vital, meaning all video segments and manifest URLs must be digitally signed with short-lived tokens to prevent ad-skipping and unauthorized stream scraping.""",
        "core_entities": """The core entities begin with the Live Event Session, which encapsulates the broadcast identifier, sport type, teams playing, and active stream metadata.

Next is the Ad Break Cue, which stores the SCTE-35 payload, the exact presentation timestamp when the break begins, and the expected duration in seconds.

We also have the Viewer Profile, containing demographic indicators, subscription tier, viewing region, and device video playback capabilities.

Then we have the Ad Pod and Ad Creative entities, where the pod represents the scheduled container of two to four individual commercial slots, and the creative represents the transcoded video segments and tracking beacon URLs.

Finally, the Playback Manifest entity represents the actual playlist document containing media chunk URIs, sequence numbers, and discontinuity tags sent to the client device.""",
        "api_design": """For the API layer, the video player initiates stream playback by calling a manifest endpoint with the event identifier and session token, receiving the master playlist containing different quality tracks.

During active playback, the player periodically polls for updated media playlist manifests every two seconds, passing the current playback sequence number and stream variant.

Internally, the SSAI manifest generator communicates with the Ad Decision Service via a low-latency gRPC call that passes the viewer's targeting tokens and the available break duration, receiving back an ordered array of ad segment URLs.

A separate telemetry beacon API receives tracking events asynchronously from the edge stitcher as each ad segment is served, logging impressions and quartiles directly into a real-time event pipeline.""",
        "data_flow": """The data flow starts when the broadcast encoder detects a commercial break signal from the stadium production truck and injects an SCTE-35 splice cue into the live transport stream.

The ingest service receives this stream, extracts the cue point, and broadcasts the upcoming ad break event with its duration to our distributed manifest manipulation cluster.

When viewers' video players make their recurring playlist poll requests to the nearest edge location, the manifest generator checks whether an ad break is active for this timestamp.

If an ad break is active, the generator looks up pre-fetched ad decisions or makes an ultra-fast lookup to the ad decision cache, stitches the appropriate ad segment URIs between discontinuity tags in the playlist, and returns the modified manifest to the viewer.

As the viewer plays through the stitched commercial segments, the edge proxy or server-side beacon emitter fires viewability and impression tracking pings to our analytics pipeline.""",
        "high_level_design": """At a high level, the architecture is split into three main layers consisting of ingest and cue detection, edge manifest manipulation, and the core ad decisioning plane.

At the front, Prime Video live encoders stream video into AWS Elemental MediaLive, where SCTE-35 splices are detected and normalized into event messages published to a high-speed Redis cluster.

In the middle layer, CloudFront edge workers or regional SSAI proxy clusters intercept incoming manifest requests from millions of active player sessions.

These proxy instances maintain lightweight in-memory session states and consult an ad decisioning service backed by distributed Redis caches to grab personalized ad pods without querying relational databases.

Pre-transcoded ad creatives are pre-warmed across global S3 buckets and edge CDNs, ensuring that when an ad is stitched, every video segment is already encoded into the identical resolutions and bitrates as the live game feed.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, handling the sudden surge of fifteen million concurrent viewers requires aggressive pre-decisioning and edge caching. Instead of waiting for the exact second the commercial break starts to compute ad decisions, our system uses predictive pre-fetching so that candidate ad pods are already calculated and cached thirty seconds before the referee signals a break.

To meet our strict fifty-millisecond latency budget, manifest manipulation is performed entirely in memory at the edge using lightweight C++ or Rust workers running in AWS Lambda@Edge or regional container clusters, bypassing disk storage and complex relational lookups.

For broadcast-grade fault tolerance, if an ad decision service fails to return a result within twenty milliseconds, the manifest generator automatically falls back to a pre-cached slate video segment or a default Prime Video promo reel, guaranteeing that viewers never experience a black screen or buffering wheel.

To maintain perfect video synchronization across different devices, all stitched ad chunks are normalized using frame-accurate segment splitters that align presentation timestamps, preventing audio drift and video lip-sync errors when transitioning between the football game and commercial breaks."""
    },

    # Q2: Real-Time Ad Auction and Header Bidding Engine
    {
        "id": 2,
        "title": "Ultra-Low Latency Real-Time Ad Auction and Bidding System",
        "category": "Real-Time Bidding & Ad Auctions",
        "problem_statement": """Design a real-time bidding and auction engine for live sports advertising that solicits bids from internal Amazon DSP and external third-party demand partners, executes a second-price or first-price auction, enforces advertiser category separation, and selects the winning creative within an uncompromising forty-millisecond SLA.""",
        "clarifying_questions": """To start, I want to clarify the exact latency budget for the entire auction cycle. In live broadcast advertising, the entire round-trip time from receiving the ad request to returning the winning creative cannot exceed forty milliseconds, which means downstream DSPs only have about twenty to twenty-five milliseconds to respond.

I would also ask about the auction mechanics and pricing model. We should clarify whether we are running a generalized first-price auction or a second-price auction, and whether we need to enforce floor prices that vary based on game score, team popularity, or viewership spikes.

Another crucial question is how many external demand partners and internal DSPs we are fanning out to simultaneously. If we fan out to twenty DSPs across the internet, network jitter can easily breach our SLA, so we need to know whether server-to-server direct fibers or regional co-location are in place.

Lastly, I would clarify competitive separation rules, such as ensuring that two rival car companies do not win slots in the same commercial break pod.""",
        "svg_diagram": generate_svg(
            "Ultra-Low Latency Real-Time Auction Engine",
            [
                ["Bid Request Router", "P99 Fanout Manager"],
                ["Demand Connectors", "Direct Fiber to DSPs"],
                ["Auction Evaluator", "Floor & Rules Engine"],
                ["Category Separator", "Pod Collision Filter"],
                ["Winning Creative", "Signed Response Token"]
            ]
        ),
        "functional_requirements": """Functionally, the auction engine must parse incoming bid opportunities originating from the SSAI service and enrich them with viewer contextual attributes, stream category, and floor pricing constraints.

The engine must then fan out bid requests in parallel to all eligible demand-side platforms and internal Amazon advertising channels over low-latency network connections.

It must collect all incoming bids that arrive before the strict timeout deadline, filtering out any bids that fail reserve price thresholds or violate advertiser brand safety rules.

The system must then execute the auction algorithm to pick the winning bid, determine the clearing price, verify competitive brand separation across the entire ad pod, and return the winning creative URL.""",
        "non_functional_requirements": """In terms of non-functional requirements, the absolute highest priority is meeting the strict forty-millisecond P99 latency SLA, because any bid evaluation that exceeds this window is discarded to prevent broadcast delay.

The system must scale horizontally to handle throughput spikes of up to one million auction evaluations per second during peak live sporting events like the Super Bowl or NBA Finals.

High availability must reach 99.999 percent, meaning the auction platform must have automatic failover to local fallback ads if upstream network connections to third-party DSPs degrade.

Data consistency for budget pacing must be maintained so that advertisers do not overspend their allocations within fractions of a second during high-volume spikes.""",
        "core_entities": """The primary core entity is the Auction Request, which holds the unique auction identifier, ad slot duration, screen dimensions, viewer segment keys, and reserve floor price.

The next entity is the Demand Partner Profile, which specifies the network endpoint, connection pool settings, timeout thresholds, and cryptographic credentials for each DSP.

We also have the Bid Submission entity, containing the DSP identifier, bid amount in cost-per-mille, target creative identifier, and brand category classification.

Another entity is the Ad Pod Rule, which governs minimum spacing between identical brand categories and maximum allowed total duration for the break.

Finally, the Auction Result entity records the winning advertiser, clearing price, timestamp, and audit log token for billing reconciliation.""",
        "api_design": """The auction service exposes an internal high-speed gRPC interface for the SSAI manifest stitcher called ExecuteAuction, which accepts the viewer context, slot duration, and current pod state, returning the chosen creative and price.

For external DSPs, the platform implements an optimized OpenRTB compliant JSON or Protobuf payload over persistent HTTP/2 or gRPC connections, sending bid requests with a hard deadline header.

There is also a management API for advertisers and account executives to configure campaign floor prices, targeting rules, and category separation restrictions in real time.

Finally, a streaming event API publishes all auction bid metrics and clearing telemetry to an event bus for real-time monitoring and reporting.""",
        "data_flow": """The data flow begins when an ad break opportunity arrives at the auction service from the SSAI engine, containing information about the upcoming slot and the viewer's anonymous profile.

The auction service enriches the request with real-time floor prices stored in an in-memory cache and initiates an asynchronous fan-out to all registered DSPs simultaneously.

Each DSP evaluates the bid request and returns its bid along with creative metadata over pre-warmed connection pools within twenty milliseconds.

A scatter-gather coordinator collects the bids, trims any late responses that miss the deadline, validates the remaining bids against floor prices, and applies second-price or first-price auction logic.

The winning bid is checked against the active ad pod to ensure no conflicting advertiser categories exist, after which the winning creative URL is returned to the SSAI stitcher, and an auction win log is streamed to Kafka.""",
        "high_level_design": """At a high level, the auction architecture consists of a high-throughput API gateway, a distributed auction orchestrator, and an in-memory caching and pacing layer.

Incoming requests hit an Envoy-based proxy fleet that routes traffic using low-overhead gRPC to auction orchestrator worker pods deployed across Kubernetes clusters in multiple AWS regions.

The orchestrator utilizes non-blocking asynchronous event loops implemented in C++ or Go, dispatching bid requests across persistent connection pools directly to DSPs.

A Redis cluster running in memory maintains real-time advertiser pacing limits and floor price tables with sub-millisecond read access.

Downstream winning bids and transaction audit trails are decoupled from the real-time path by immediately dumping event payloads into Apache Kafka topics for asynchronous financial settlement and analytics.""",
        "nfr_deep_dive": """Taking a deep dive into the non-functional requirements, managing the forty-millisecond latency SLA requires aggressive connection pooling and strict circuit breaking. Every connection to an external DSP is maintained over pre-warmed HTTP/2 connections with TCP keep-alive, eliminating the latency penalty of TLS handshakes during live games.

The scatter-gather coordinator sets a rigid twenty-five millisecond hard timer. As soon as that timer expires, the coordinator proceeds immediately with whatever bids have already arrived, completely ignoring any late packets without waiting or retrying.

If a specific DSP exhibits consecutive timeouts or latency spikes, an automated circuit breaker trips and temporarily stops sending traffic to that partner for sixty seconds, protecting the overall system from thread starvation.

To prevent advertiser overspending during sudden viewership surges, real-time budget decrements are tracked in Redis using atomic Lua scripts with probabilistic pacing algorithms, ensuring budget allocations are smoothly consumed without locking database rows."""
    },

    # Q3: Real-Time Ad Pacing and Global Budget Smoothing
    {
        "id": 3,
        "title": "Real-Time Ad Pacing and Global Budget Smoothing Engine",
        "category": "Ad Pacing & Optimization",
        "problem_statement": """Design a distributed ad pacing and budget smoothing service that prevents advertisers from exhausting their daily or game-long campaign budgets in the first quarter of a live sporting event. The system must adaptively throttle or accelerate bid participation rates across millions of real-time impressions based on game progression, quarter pacing, and viewer fluctuations.""",
        "clarifying_questions": """When clarifying this design, my first question is about the pacing model: are we pacing budgets evenly across wall-clock time, or are we pacing dynamically based on game progression like quarters, halves, and potential overtime? Because live sports have unpredictable game lengths and viewing spikes, pacing must adjust based on live game telemetry rather than a simple clock.

Next, I would ask about the acceptable delay for budget synchronization. Can pacing parameters be calculated asynchronously every few seconds and pushed to edge auction nodes, or does every single impression need an immediate atomic counter decrement? Calculating probabilistic pacing probabilities every few seconds is the industry standard to protect auction latency.

I would also clarify the scale of active campaigns. We need to know if we are managing ten thousand campaigns or hundreds of thousands of concurrent ad lines across multiple live sporting events simultaneously.

Finally, I would ask how the system handles surprise blowouts or overtime scenarios where viewership suddenly collapses or skyrockets unexpectedly.""",
        "svg_diagram": generate_svg(
            "Real-Time Ad Pacing & Budget Smoothing",
            [
                ["Live Game Telemetry", "Game Clock & Viewers"],
                ["Pacing Controller", "PID & Trajectory Math"],
                ["Edge Probability Cache", "Sub-Millisecond Sync"],
                ["Auction Filter", "Probabilistic Bid Drop"],
                ["Budget Ledger", "Stream Count Aggregator"]
            ]
        ),
        "functional_requirements": """Functionally, the pacing system must track the real-time spend of every advertising campaign and compare it against its assigned target budget trajectory for the specific live event.

It must ingest real-time live game status updates, including current quarter, remaining game time, score differentials, and current viewer counts, to dynamically adjust expected future impression inventory.

The system must compute a dynamic bid pass-through probability between zero and one for every active campaign and distribute these parameters to auction nodes.

When an ad slot opportunity occurs, the auction filter evaluates the campaign's current probability using a random coin flip, deciding whether to submit a bid or sit out to conserve budget.

It must also provide an administrative dashboard allowing campaign managers to manually accelerate spend or inject emergency budget additions during the game.""",
        "non_functional_requirements": """From a non-functional perspective, the evaluation of pacing decisions at auction time must happen in under one millisecond to fit within the broader forty-millisecond auction SLA.

Budget overspend must not exceed one percent of the advertiser's total allocated cap, even during extreme viewership spikes when millions of viewers hit a commercial break at once.

The pacing calculation service must be fault-tolerant and capable of surviving node crashes without losing track of accumulated spend.

The system must scale effortlessly to manage thousands of active advertising campaigns simultaneously across dozens of concurrent live broadcast streams.""",
        "core_entities": """The primary core entity is the Campaign Budget Specification, defining the total budget, daily limit, target sporting event, and preferred pacing profile such as even, front-loaded, or late-game focused.

Another entity is the Game State Tracker, capturing the current quarter, game clock, home and away scores, and live concurrent stream count.

We also have the Accumulated Spend Ledger, which records confirmed impressions, total dollar spend, and remaining balance for each campaign.

Then there is the Pacing Rate Entity, which stores the calculated bid participation probability, timestamp of calculation, and target spend velocity for the upcoming five-second window.

Finally, the Budget Adjustment Event entity logs manual budget top-ups, campaign suspensions, and post-game reconciliation records.""",
        "api_design": """The service provides a configuration API for advertisers to set campaign budgets, flight dates, and pacing preferences using standard REST endpoints.

For the auction engine, the service provides an ultra-fast local memory lookup API that returns whether a campaign is eligible to bid based on its pre-calculated pass-through probability.

There is an internal stream ingestion API that consumes real-time impression confirmation events from Kafka topics to continuously update campaign spend balances.

Finally, a metrics API exposes current spend trajectories, burn rates, and projected completion percentages to internal monitoring tools and advertiser dashboards.""",
        "data_flow": """The data flow begins when impression confirmation beacons are recorded by the ad serving fleet as viewers watch commercial breaks.

These beacons are published to an Apache Kafka impression topic, where stream processing jobs aggregate spend metrics in near real time across five-second sliding windows.

The aggregated spend is written into an in-memory Redis cluster that maintains the current cumulative spend for every campaign.

Concurrently, a centralized Pacing Calculation Service reads the cumulative spend, compares it against the campaign's target spend curve and live game clock telemetry, and runs a control algorithm to compute updated bidding probabilities.

These new bidding probabilities are broadcast every two seconds to the local memory of all auction worker nodes, which use them to filter candidate bids instantaneously.""",
        "high_level_design": """At a high level, the pacing platform is decoupled into a fast-path local evaluation layer and a background control loop.

On the auction worker nodes, each server keeps an in-memory dictionary of campaign IDs mapped to their current bid participation probability, allowing zero-latency local checks without any network calls.

In the background, an Apache Flink streaming pipeline ingests verified impression events from Kafka, summing up dollar spend per campaign across all global regions.

A centralized Pacing Engine implemented as a Python and FastAPI service reads these real-time spend numbers from Redis and ingests sports metadata from an official sports radar feed.

The Pacing Engine executes a Proportional-Integral-Derivative control algorithm to recalibrate bidding probabilities, pushing updates back to all auction nodes via Redis Pub/Sub or high-performance gRPC channels.""",
        "nfr_deep_dive": """Diving deep into non-functional requirements, preventing budget overspend during explosive viewership spikes requires a combination of feedback control loops and safety margins. When a dramatic game moment occurs, such as a game-winning drive in the fourth quarter, viewership can double within minutes, causing burn rates to surge unpredictably.

To counteract this, our PID controller incorporates a derivative term that detects the acceleration of spend, automatically dialing back bidding probabilities before the budget ceiling is breached.

Furthermore, we implement a soft reserve buffer where the pacing engine targets spending only ninety-eight percent of the allocated budget during normal pacing calculations, reserving the final two percent as a shock absorber for in-flight requests.

To guarantee sub-millisecond evaluation at auction time, auction nodes never query a central database to check budget balance. Instead, they perform a purely local pseudorandom check against their synchronized probability cache, completely eliminating database contention under heavy load."""
    },

    # Q4: Real-Time Frequency Capping & Competitive Separation
    {
        "id": 4,
        "title": "Real-Time Ad Frequency Capping and Competitive Separation Service",
        "category": "Ad Targeting & Business Rules",
        "problem_statement": """Design a real-time frequency capping and competitive separation service for live sports broadcasts on Prime Video. The system must ensure that a single viewer does not see the same commercial more than twice during a live game, while simultaneously ensuring that competing advertisers (such as two rival automotive brands) are never scheduled in the same ad pod or back-to-back across adjacent breaks.""",
        "clarifying_questions": """To properly frame this system, I would first clarify the scope of frequency capping. Is the frequency cap enforced strictly per viewer device, per user account across multiple devices, or globally across a household IP address? Usually, enforcing caps at the authenticated Amazon user account level is preferred, with a fallback to anonymous device IDs.

Next, I would ask about the time window for the cap. Does the frequency limit apply strictly within a single three-hour football broadcast, or does it span a full twenty-four hour day or entire week of live sports programming? For live events, in-game frequency capping is the most critical constraint to avoid viewer fatigue.

I would also clarify the taxonomy and depth of competitive separation. How are product categories structured, and can an advertiser request brand-level separation, parent company separation, or specific competitor blacklists?

Finally, I would ask about latency constraints. Because this check sits directly in the ad decision path, the lookup and validation of frequency rules must complete in under five milliseconds.""",
        "svg_diagram": generate_svg(
            "Frequency Capping & Competitive Separation",
            [
                ["Ad Decision Request", "User & Slot Context"],
                ["User Ad History", "Redis Sliding Bitmaps"],
                ["Category Conflict Map", "In-Memory Graph"],
                ["Pod Builder Engine", "Slot Conflict Resolver"],
                ["Filtered Ad Pod", "Compliant Playlist"]
            ]
        ),
        "functional_requirements": """Functionally, the system must record every ad impression delivered to a specific viewer account, tracking which creative, brand, and product category was shown along with the timestamp.

When an ad decision is being prepared for an upcoming break, the service must query the viewer's recent ad history and filter out any candidate ads that have already reached their frequency threshold.

The service must also inspect the candidate ads chosen for a multi-slot ad pod and evaluate them against our competitive separation matrix, verifying that no two ads belong to the same restricted category.

In addition, it must verify pod-to-pod separation rules, preventing a car ad placed in the final slot of one commercial break from being followed by another car ad in the first slot of the subsequent break.

It must also support customizable frequency policies configured by advertisers, such as maximum three impressions per game and at least thirty minutes of separation between showings.""",
        "non_functional_requirements": """For non-functional requirements, the entire lookup and validation process must execute in under five milliseconds to keep the ad decisioning pipeline within its overall budget.

The system must handle high write throughput, recording millions of ad impression events per minute during commercial breaks without data loss or significant lag.

Data consistency must be strong enough within a user's session to ensure that an ad shown sixty seconds ago is immediately reflected in the user's history before the next break is assembled.

The storage footprint must remain optimized and cost-effective, pruning expired viewer history as soon as the live sporting event concludes.""",
        "core_entities": """The first core entity is the Viewer Impression History, which maps a user identifier to a list of recently watched creative IDs, brand IDs, and timestamps.

Next is the Brand Entity, capturing the advertiser ID, parent company ID, and assigned industry classification code such as Automotive, Insurance, or Fast Food.

We also have the Competitive Separation Rule entity, defining which industry categories or specific brand pairs cannot be displayed within the same pod or within a given time window.

Then there is the Ad Pod Slot Specification, describing the ordered positions within a commercial break and any positional restrictions such as first-in-pod or last-in-pod preferences.

Finally, the Frequency Cap Policy entity defines the maximum allowable exposures per user across specific time intervals.""",
        "api_design": """The service provides an internal gRPC method called ValidateAndFilterCandidates, where the ad decision engine submits a user ID, break duration, and a list of candidate ads, receiving back a filtered list of eligible creatives.

Another gRPC method named CommitPodSchedule temporarily reserves the selected ads for a viewer session to prevent race conditions while the manifest is being assembled.

There is also an asynchronous ingestion endpoint that consumes verified impression beacons from Kafka to permanently record completed impressions in the user's history.

Additionally, a configuration API allows operations teams and advertisers to update brand category taxonomies and competitive separation pairs dynamically.""",
        "data_flow": """The data flow starts when the ad decision engine receives a request to populate a commercial break for a specific viewer.

The decision engine calls the Frequency Capping Service via gRPC, passing the viewer ID and the pool of potential winning ad creatives.

The service performs an in-memory lookup against a distributed Redis cluster using the user ID as the key, retrieving the compact list of creative and brand IDs the user has seen during this broadcast.

Any candidate that breaches frequency caps is discarded, and the remaining candidates are evaluated by a pod layout algorithm that checks for category collisions against our pre-loaded competitive separation matrix.

Once a valid, collision-free ad pod is composed, the tentative selection is returned to the decision engine, and upon playback confirmation, an impression beacon updates the viewer's history in Redis.""",
        "high_level_design": """At a high level, the architecture utilizes an ultra-fast in-memory caching tier combined with an asynchronous stream processing pipeline.

The core lookup engine runs as a stateless Go or C++ microservice deployed in Kubernetes, capable of evaluating complex separation matrices against user history in microseconds.

User history is stored in an in-memory Redis cluster partitioned by user ID, utilizing compact data structures such as Redis Hashes and Sorted Sets with automatic TTL expiration tied to the event duration.

The competitive category separation graph is relatively static and small, so it is cached directly in the local memory of each service instance and updated via background publish-subscribe channels.

Impression events emitted from video players or edge manifest generators flow through Apache Kafka into a stream ingestion worker that writes confirmed views into the Redis cache asynchronously.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, achieving sub-five-millisecond response times at massive scale requires minimizing serialization overhead and network hops. We store each user's viewing history in Redis using compact bitsets or sorted sets containing only 64-bit integer hashes of creative IDs and category codes rather than full JSON blobs.

To handle race conditions where back-to-back ad requests for the same user occur within seconds, the service implements short-lived optimistic reservations in Redis with a ten-second TTL, preventing duplicate ad selections while the manifest is being stitched.

To maintain high availability and prevent cache outages from halting the live broadcast, the service employs a graceful degradation strategy: if the Redis user history lookup times out, the service relaxes personal frequency caps while continuing to enforce strict competitive category separation within the current pod.

Storage optimization is maintained by setting an automatic four-hour time-to-live on all in-game user viewing records, ensuring that memory across the Redis cluster is automatically recycled as soon as the live football game concludes."""
    },

    # Q5: Impression Tracking & Viewability Beacon Collector
    {
        "id": 5,
        "title": "Server-Side Ad Impression Tracking and Viewability Beacon Collector",
        "category": "Telemetry & Measurement",
        "problem_statement": """Design a highly resilient, large-scale ad impression tracking and viewability beacon collection pipeline for Prime Video live events. The system must ingest, validate, deduplicate, and process hundreds of millions of tracking pings emitted by edge manifest servers and client video players during commercial breaks, guaranteeing exactly-once attribution and audit-ready billing records for advertisers.""",
        "clarifying_questions": """When beginning this design, I would first clarify whether beacons originate from client video players, edge manifest servers, or both. In live broadcasting, a hybrid approach is common: edge servers emit delivery beacons when segments are served, while client video players emit start, midpoint, and completion viewability beacons as the viewer watches the screen.

Next, I would ask about the expected peak request rate. If fifteen million viewers transition from content to an ad break at the exact same second, we could experience a sudden surge of tens of millions of HTTP beacon requests within a five-second window.

I would also clarify the data freshness requirements for billing and analytics dashboards. Do advertisers expect real-time spend dashboards within seconds, or is an hourly reconciliation pipeline acceptable for final billing audits?

Finally, I would ask about compliance standards, such as Media Rating Council viewability guidelines and fraud detection checks like filtering out bot traffic and duplicate pings.""",
        "svg_diagram": generate_svg(
            "Ad Impression & Viewability Beacon Pipeline",
            [
                ["Edge Beacon Ingest", "Global CloudFront Fleet"],
                ["Ingest Gateway", "Validation & Sig Verify"],
                ["Apache Kafka", "Partitioned Event Log"],
                ["Flink Deduplicator", "RocksDB State Store"],
                ["ClickHouse / Druid", "Audit-Ready Analytics"]
            ]
        ),
        "functional_requirements": """Functionally, the beacon collector must accept incoming HTTP GET and POST tracking requests from both edge manifest generators and client video playback SDKs.

It must decrypt and validate cryptographically signed beacon payloads to verify that the tracking event originated from a legitimate Prime Video session and has not been forged or altered.

The system must track multiple lifecycle milestones for each ad playback, including impression start, first quartile, midpoint, third quartile, complete view, and any user mute or pause interactions.

It must perform real-time deduplication to ensure that network retries or player bugs do not register duplicate billable impressions for the same viewing event.

Finally, it must deliver enriched, aggregated impression metrics to real-time advertiser reporting dashboards and write immutable raw logs to long-term storage for financial auditing.""",
        "non_functional_requirements": """On the non-functional side, high throughput ingestion is the primary challenge, requiring the system to absorb surges of over twenty million requests per minute without dropping a single valid beacon.

The ingestion endpoint must respond with an HTTP 200 or 204 status within fifteen milliseconds to release client connections and prevent connection pooling bottlenecks.

Data durability must be 99.999999999 percent, as every verified impression represents contractual advertising revenue that cannot be lost.

The system must guarantee exactly-once processing semantics for all financial and billing aggregations, even in the event of worker node restarts or network partitions.""",
        "core_entities": """The primary core entity is the Tracking Beacon Event, which contains the unique beacon token, session ID, creative ID, campaign ID, timestamp, milestone type, and device metadata.

Next is the Signed Beacon Token, which holds encrypted payload data containing the auction ID, clearing price, viewer hash, and expiration timestamp generated during ad selection.

We also have the Verified Impression Record, representing an authenticated, deduplicated impression event ready for billing and attribution calculation.

Another entity is the Viewability Session, tracking the sequential progression of milestones for a specific ad display from start to completion.

Finally, the Advertiser Billing Aggregate entity maintains accumulated billable impression counts and dollar amounts grouped by campaign and time interval.""",
        "api_design": """The public ingestion API exposes lightweight HTTP endpoints such as /beacon/v1/track, accepting signed query parameters or compact JSON payloads from clients and edge servers.

The endpoint immediately responds with an HTTP 204 No Content header upon successfully queuing the event, minimizing round-trip overhead.

Internally, stream processing workers use an event schema defined in Apache Avro or Protocol Buffers to serialize beacon records before publishing to Kafka.

A private GraphQL or REST reporting API allows advertiser portals and operations dashboards to query aggregated metrics like impression counts, completion rates, and effective cost-per-mille in real time.""",
        "data_flow": """The data flow begins when a viewer's video player reaches an ad playback milestone or an edge server dispatches an ad chunk, triggering an HTTP tracking ping to our edge CDN.

The CDN terminates the TLS connection and routes the request to an API Gateway fleet deployed across regional AWS points of presence.

The gateway performs cryptographic signature verification on the beacon token, adds a server reception timestamp, and writes the raw event directly into a regionally partitioned Apache Kafka topic.

Apache Flink stream processing applications consume events from Kafka, using keyed state backed by RocksDB to deduplicate incoming beacons against the unique auction and token identifier within a ten-minute sliding window.

Deduplicated impression events are simultaneously streamed to an OLAP database like ClickHouse or Apache Pinot for instant dashboard queries and archived into Amazon S3 for permanent audit trails.""",
        "high_level_design": """At a high level, the architecture consists of an edge ingestion layer, a distributed message buffering bus, a stateful stream processing cluster, and analytical data stores.

The edge layer utilizes Amazon CloudFront and an Auto Scaling group of lightweight Rust or Go ingest proxies behind Network Load Balancers to handle massive concurrent socket connections.

The message bus is built on high-throughput Apache Kafka clusters, partitioned by user ID or session ID to ensure all events for a single viewer session are processed sequentially by the same consumer group.

The stream processing layer is powered by Apache Flink, which manages in-memory deduplication state, sessionizes ad milestone progressions, and generates real-time metric aggregations.

The persistent storage tier pairs Amazon S3 parquet data lakes with ClickHouse for sub-second analytical queries across billions of daily historical impressions.""",
        "nfr_deep_dive": """Taking a deep dive into the non-functional requirements, ensuring exactly-once processing amidst massive traffic bursts requires robust stream processing architecture. Flink achieves exactly-once semantics by combining Kafka offset tracking with distributed asynchronous checkpointing to Amazon S3 using the Chandy-Lamport algorithm.

To handle the immense deduplication workload without exhausting memory, Flink uses RocksDB-backed state stores keyed on the composite token of session ID and creative ID, configured with a fifteen-minute state time-to-live that safely catches all realistic client retry attempts.

To insulate our ingestion pipeline from unexpected traffic spikes during thrilling game overtimes, the ingest gateway performs zero complex business logic or synchronous database writes. Its sole responsibility is signature validation and appending bytes to the Kafka log, allowing each gateway instance to sustain over fifty thousand requests per second.

In the event of a downstream analytics database slowdown, Kafka acts as an elastic buffer holding hours of raw beacon telemetry, guaranteeing that no advertiser impressions are lost while the downstream analytical engines recover."""
    },

    # Q6: Autonomous Live Broadcast Incident Detection & Auto-Remediation Agent (MCP)
    {
        "id": 6,
        "title": "Autonomous Live Broadcast Incident Remediation Agent using Model Context Protocol",
        "category": "AI Agents & Autonomous Operations",
        "problem_statement": """Design an autonomous AI operations agent powered by large language models and the Model Context Protocol (MCP) to monitor live broadcast advertising pipelines during events like Thursday Night Football. The agent must detect real-time stream anomalies, diagnose root causes across microservices, and safely execute approved remediation actions like traffic shifting or restarting stuck transcoders without human delay.""",
        "clarifying_questions": """To properly scope this autonomous operations agent, I would first ask about the boundaries of autonomy. What actions is the agent permitted to execute completely autonomously, and which actions require human engineer confirmation via an emergency Slack or pager interface? High-risk actions like restarting an entire database cluster should require human approval, while low-risk actions like rerouting traffic or restarting a single stuck worker can be autonomous.

Next, I would ask about the telemetry sources available to the agent. Does the system have access to distributed OpenTelemetry traces, real-time CloudWatch metrics, application logs, and live video quality monitors? The richer the context, the better the agent's reasoning.

I would also clarify the latency requirement for incident detection and action execution. In a live sporting event, an undetected ad glitch lasting two minutes can cost millions of dollars, so the agent must detect and remediate anomalies within sixty seconds.

Finally, I would ask how MCP servers are structured across the organization and what security sandboxing is in place to prevent hallucinated or dangerous command executions.""",
        "svg_diagram": generate_svg(
            "Autonomous Broadcast Incident AI Agent (MCP)",
            [
                ["Telemetry Stream", "Metrics, Logs & Traces"],
                ["Anomaly Detector", "Dynamic Threshold Alert"],
                ["LLM Reasoning Core", "Claude / Bedrock Agent"],
                ["MCP Tool Orchestrator", "Safe Action Execution"],
                ["Broadcast Infrastructure", "Auto-Remediated State"]
            ]
        ),
        "functional_requirements": """Functionally, the autonomous agent must continuously ingest real-time operational telemetry, including manifest error rates, SSAI latency spikes, ad auction timeouts, and video frame drop counts.

When an anomaly is flagged, the agent must inspect the event context, formulate a hypothesis, and use MCP tool interfaces to query relevant microservice logs and distributed traces.

The agent must synthesize the gathered evidence to pinpoint the root cause, such as a failing transcoder instance, a misconfigured third-party DSP endpoint, or a saturated database connection pool.

It must then look up pre-approved operational runbooks, select the appropriate remediation strategy, and execute the corrective actions through dedicated MCP tool connectors.

Finally, it must verify that the remediation successfully resolved the issue, generate a structured incident summary, and notify on-call engineers in the broadcast operations channel.""",
        "non_functional_requirements": """On the non-functional side, safety and determinism are paramount: the agent must operate within strict guardrails to ensure that an LLM hallucination cannot trigger catastrophic configuration changes or accidental stream shutdowns.

The entire detection, diagnosis, and remediation loop must complete in under sixty seconds to prevent viewers from experiencing prolonged stream disruptions during commercial breaks.

Auditability is critical, requiring that every step of the agent's thought process, tool invocations, parameters, and system responses be immutably logged for post-incident review.

The agent infrastructure must maintain high availability and run independently from the broadcast data path so that operational failures in the ad pipeline do not bring down the monitoring agent.""",
        "core_entities": """The primary core entity is the Incident Context, capturing the alert timestamp, affected broadcast property, severity level, impacted viewers, and initial anomaly telemetry.

Next is the MCP Tool Definition, specifying available operational commands like query_logs, inspect_traces, restart_service_pod, and divert_traffic, along with strict JSON schemas for input parameters.

We also have the Reasoning Trace entity, which stores the LLM's step-by-step chain of thought, hypothesis validations, tool call arguments, and tool outputs.

Another entity is the Remediation Action Plan, outlining the selected runbook steps, safety classification, authorization requirements, and rollback criteria.

Finally, the Post-Incident Summary entity encapsulates the timeline, root cause diagnosis, actions taken, and verification metrics formatted for human review.""",
        "api_design": """The agent interacts with underlying infrastructure through standardized Model Context Protocol (MCP) server endpoints running over secure JSON-RPC or gRPC connections.

It provides a query API for on-call engineers to inspect current agent reasoning or manually prompt the agent with questions like What caused the latency spike in US-East during the halftime break?

There is an inbound webhook API that receives high-priority anomaly alerts from CloudWatch, Prometheus, and video quality monitoring systems to wake the agent.

The agent also exposes an interactive Slack or Teams bot integration API where it posts diagnostic updates and provides one-click approval buttons for actions requiring human confirmation.""",
        "data_flow": """The data flow begins when an anomaly detection engine identifies that the SSAI manifest generation latency has exceeded eighty milliseconds for three consecutive intervals.

The anomaly detector dispatches a high-priority alert payload to the Autonomous Agent Core via an event queue.

The agent initializes an incident context and invokes an MCP telemetry tool to pull recent error logs and distributed traces from OpenSearch and AWS X-Ray.

The LLM analyzes the logs, identifies that an external DSP is hanging on TCP connections and causing worker thread exhaustion, and decides to isolate the offending endpoint.

The agent invokes the MCP Traffic Controller tool to disable bidding for that specific partner, verifies through follow-up telemetry that manifest latencies have dropped back to twenty milliseconds, and posts an incident debrief to Slack.""",
        "high_level_design": """At a high level, the architecture combines event-driven telemetry ingest, an LLM orchestration layer running on Amazon Bedrock, and a fleet of secure MCP tool servers.

Alerts from Prometheus and AWS CloudWatch are pushed into an Amazon SQS queue that feeds the Agent Orchestrator service built with Python and LangGraph.

The orchestrator leverages Claude 3.5 Sonnet or Amazon Bedrock foundation models with custom system prompts that enforce structured thinking and safety policies.

The agent communicates with internal systems strictly through a dedicated MCP Gateway that hosts isolated MCP servers for AWS Kubernetes control, CloudFront CDN management, and database telemetry.

A dedicated Policy Guardrail layer intercepts every tool call emitted by the LLM, validating that arguments adhere to whitelisted ranges and safety rules before forwarding them to production infrastructure.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, ensuring operational safety during live sports broadcasts requires multiple layers of defense-in-depth. We enforce a strict Tiered Autonomy Matrix where low-risk actions like shifting traffic away from an unhealthy container or clearing a local cache are executed autonomously, while high-risk actions like scaling down core clusters or changing global routing require human confirmation via Slack within a two-minute window.

To prevent infinite execution loops or erratic behavior, the agent is bounded by a maximum tool recursion depth of five steps and a strict ninety-second overall execution deadline.

Every MCP tool call is validated against a deterministic JSON schema validator, rejecting any malformed or unexpected parameters before they reach operational APIs.

Furthermore, every remediation action has an automatic rollback mechanism: if key metrics do not show measurable improvement within thirty seconds of executing an action, the agent automatically reverts the change and immediately escalates the incident to human on-call leads.""",
    },

    # Q7: Real-Time Video Scene & Brand Safety Classification (VLA / Multimodal AI)
    {
        "id": 7,
        "title": "Real-Time Video Scene and Brand Safety Classification Pipeline for Live Sports",
        "category": "Multimodal AI & Computer Vision",
        "problem_statement": """Design a real-time computer vision and multimodal AI pipeline that analyzes incoming live sports video frames and audio transcripts to classify game scenes (such as player injuries, fights, or controversial referee reviews) within five hundred milliseconds. The system must prevent brand-sensitive advertisements (like airline or insurance ads) from running alongside tragic or violent live broadcast moments.""",
        "clarifying_questions": """To clarify the system requirements, I would first ask about the frame rate and sampling frequency needed for video analysis. Analyzing thirty frames per second with heavy vision models is computationally prohibitive, so we should establish whether sampling one or two keyframes per second combined with live audio transcripts provides sufficient accuracy.

Next, I would ask about the exact latency SLA from frame capture to brand safety classification. If an ad break cue occurs immediately following a severe player injury, the classification tag must be published within five hundred milliseconds so the ad decision engine can block sensitive advertisers.

I would also clarify the taxonomy of sensitive events. Does the model need to distinguish between sports celebration tackles versus real violent brawls, and does it need to detect text overlays like Breaking News banners using optical character recognition?

Finally, I would ask about infrastructure constraints, such as the availability of GPU clusters at broadcast ingest points and fallback behavior if the AI pipeline experiences backpressure.""",
        "svg_diagram": generate_svg(
            "Real-Time Video Scene & Brand Safety AI",
            [
                ["Live Video Feed", "Frame & Audio Extractor"],
                ["Multimodal AI Model", "Vision + Whisper OCR"],
                ["Brand Safety Classifier", "Safety & Context Scores"],
                ["Low-Latency Event Bus", "Sub-50ms Redis State"],
                ["Ad Decision Engine", "Contextual Ad Filter"]
            ]
        ),
        "functional_requirements": """Functionally, the system must continuously ingest the live broadcast video stream, decoding keyframes at regular intervals and extracting the concurrent closed-caption and commentator audio track.

The pipeline must pass extracted frames and audio tokens through a multimodal AI model to classify the current emotional tone, scene activity, and presence of sensitive content like medical emergencies or aggressive altercations.

It must generate normalized brand safety risk scores across standard industry categories such as violence, injury, tragedy, and political controversy.

The service must publish updated safety tags into a sub-millisecond in-memory cache accessible to the ad decision engine before every commercial break.

It must also provide an operational dashboard displaying live model confidence scores, detected video snippets, and manual override controls for broadcast compliance monitors.""",
        "non_functional_requirements": """In terms of non-functional requirements, the end-to-end processing latency from video ingestion to tag publication must stay strictly under five hundred milliseconds to ensure tags are available before ad selection begins.

The system must maintain high classification precision to avoid false alarms that unnecessarily block high-paying premium advertisers during normal game play.

Availability must reach 99.99 percent throughout the live event, with the pipeline deployed across redundant GPU instances to survive hardware failures.

Scalability must support parallel processing of dozens of concurrent live broadcast feeds across different sports, camera angles, and localized language commentary tracks.""",
        "core_entities": """The primary core entity is the Video Frame Sample, encapsulating the raw image bytes, timestamp, camera angle, and stream identifier.

Next is the Audio Transcript Segment, containing transcribed commentator speech, crowd noise volume levels, and closed-caption text for the corresponding time window.

We also have the Scene Classification Result entity, storing confidence scores for categories like normal game play, celebration, injury, fight, or weather delay.

Another entity is the Advertiser Brand Safety Profile, which defines which specific scene categories an advertiser refuses to appear alongside.

Finally, the Live Context State entity represents the active global safety score applied to the current broadcast timestamp, used by ad selection filters.""",
        "api_design": """The service provides a low-latency gRPC query interface called GetCurrentBroadcastContext, allowing ad decision servers to retrieve active brand safety tags in under two milliseconds.

There is a streaming ingestion API that consumes raw MPEG-TS or HLS video streams directly from broadcast encoders via low-latency SRT or RTMP protocols.

An internal event stream emits classified scene events into an Amazon Kinesis or Kafka topic whenever the safety score transitions above or below critical thresholds.

A management API allows compliance operators to register new sensitive keyword dictionaries, adjust model sensitivity thresholds, and trigger manual scene overrides in real time.""",
        "data_flow": """The data flow begins as the live broadcast feed enters a video ingest worker that samples two keyframes per second and pipes the audio stream through an automated speech recognition model.

The video frames and transcribed text are packaged into a multimodal tensor payload and submitted to a specialized Vision-Language model hosted on GPU inference clusters.

The model evaluates visual context, player body posture, on-screen medical graphics, and commentator sentiment, computing a composite brand safety risk index.

If an injury or sensitive incident is detected, the safety index spikes, and the worker immediately writes an updated safety state into a regional Redis cluster within fifty milliseconds.

When an upstream SCTE-35 ad break cue arrives moments later, the ad decision engine queries Redis, reads the high-risk safety tag, and automatically excludes sensitive advertisers from winning slots in that break.""",
        "high_level_design": """At a high level, the architecture consists of a GPU-accelerated video decoding tier, a multimodal inference cluster, an in-memory broadcast state cache, and integration hooks into the ad serving plane.

Video streams are ingested using FFmpeg workers running on AWS EC2 instances equipped with hardware video decoders to minimize CPU overhead.

Inference is executed across an Amazon SageMaker or custom Kubernetes GPU fleet running optimized TensorRT-LLM or vLLM deployments of multimodal models like CLIP and lightweight vision-language architectures.

Classified scene metadata is written directly to a distributed Redis cluster using Redis Strings with microsecond read latency.

The ad decision engine reads this Redis state synchronously on every bid evaluation, filtering candidate ad creatives against advertiser brand safety matrices before finalizing the ad pod.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, achieving sub-five-hundred-millisecond end-to-end latency while running deep neural networks requires aggressive pipeline optimization. Instead of processing full-resolution 4K or 1080p frames, the ingest worker downsamples frames to 384x384 pixels, which preserves all semantic information needed for scene classification while reducing inference compute by over eighty percent.

We employ a two-tiered hierarchical inference architecture: a lightweight, ultra-fast convolutional model runs continuously on every frame taking twenty milliseconds, and only when that model detects anomalous visual patterns does the pipeline invoke the larger multimodal vision-language model for comprehensive reasoning.

To guarantee high availability without interrupting live ad serving, the system fails open with respect to ad delivery but fails closed with respect to sensitive categories: if the AI classification pipeline encounters an unexpected crash or timeout, the ad server defaults to showing neutral, brand-safe promotional content rather than risking unvetted placements.

Redundant GPU worker nodes are deployed in an active-active configuration across multiple availability zones, ensuring instant failover with zero dropped frames if an underlying EC2 host degrades."""
    },

    # Q8: Generative AI Prompt Engineering and Evaluation Platform
    {
        "id": 8,
        "title": "Generative AI Prompt Engineering and Evaluation Platform (CI/CD for LLMs)",
        "category": "AI Infrastructure & CI/CD",
        "problem_statement": """Design a continuous integration and evaluation platform for prompt engineering and LLM tools across Amazon Advertising. The system must automatically benchmark, regression-test, and score new prompt versions, agent workflows, and model upgrades against golden datasets of live sports advertising scenarios, verifying response quality, latency, cost, and safety before production deployment.""",
        "clarifying_questions": """When framing this platform, I would first ask about the types of AI tasks being evaluated. Are we testing operational incident diagnosis prompts, dynamic ad copy generation, or natural language reporting queries? Each use case requires different evaluation metrics, such as factual precision, schema compliance, or creative tone.

Next, I would ask about the evaluation methodology. Do we rely on programmatic heuristic assertions, semantic vector similarity, or an LLM-as-a-judge architecture where an advanced model like Claude 3.5 Sonnet evaluates candidate responses against predefined rubric guidelines?

I would also clarify the scale of the evaluation suite. How many test cases exist in a typical regression run, and what is the target turnaround time for a pull-request test build? If a suite has ten thousand test cases, running them sequentially through foundation models will be slow and costly, so parallel execution and caching are necessary.

Finally, I would ask about integration with existing developer workflows, such as GitHub Actions, AWS CodePipeline, and internal model registries.""",
        "svg_diagram": generate_svg(
            "Prompt Engineering & LLM CI/CD Platform",
            [
                ["Prompt PR Commit", "GitHub / Git Hook"],
                ["Eval Orchestrator", "Parallel Test Runner"],
                ["Model Inference Fleet", "Amazon Bedrock API"],
                ["LLM-as-a-Judge", "Rubric Scoring Engine"],
                ["CI/CD Gate & Report", "Pass/Fail Deployment"]
            ]
        ),
        "functional_requirements": """Functionally, the platform must allow prompt engineers and developers to version-control prompts, tool schemas, and model configurations in Git alongside application code.

When a pull request is submitted, the evaluation engine must trigger automated test runs across curated datasets of live broadcast scenarios, edge cases, and adversarial safety prompts.

The system must execute model inference in parallel across target foundation models hosted on Amazon Bedrock or SageMaker, recording outputs, latency, and token consumption.

It must evaluate the responses using automated graders, checking strict JSON schema conformity, factual accuracy against reference ground truths, and qualitative quality via an LLM judge.

Finally, it must generate a comprehensive diff report comparing the new prompt's performance against the production baseline, automatically blocking merges if quality degrades or safety guardrails are violated.""",
        "non_functional_requirements": """From a non-functional perspective, evaluation suite execution must be fast and scalable, completing a standard hundred-case regression suite in under three minutes to prevent developer bottlenecks.

The evaluation results must be deterministic and reproducible, minimizing scoring variance from LLM judges through calibrated prompt rubrics and zero-temperature configurations.

Cost efficiency is essential, requiring intelligent caching of unchanged test case evaluations to prevent unnecessary model inference expenses during frequent CI runs.

The system must maintain high security, ensuring that test prompts containing proprietary ad business logic and customer data never leak into public model training sets.""",
        "core_entities": """The primary core entity is the Prompt Template, defining the parameterized system prompt, user prompt template, model hyperparameters, and associated tool specifications.

Next is the Golden Dataset, consisting of curated test inputs, expected output characteristics, reference reasoning traces, and safety boundary cases.

We also have the Evaluation Run entity, tracking the commit hash, author, target model identifier, execution timestamp, and aggregate pass-fail status.

Another entity is the Grader Rubric, which defines scoring criteria such as correctness, conciseness, hallucination penalty, and schema adherence on a one-to-five scale.

Finally, the Benchmark Comparison Report entity captures side-by-side performance deltas between the baseline prompt and the candidate prompt.""",
        "api_design": """The platform provides a CLI and REST API for triggering evaluation runs, allowing developers to execute test suites locally or from CI/CD pipelines with simple commands.

There is a web-based playground API that allows engineers to experiment interactively with prompts, inspect live model outputs, and compare responses across different model versions side by side.

An internal webhook receiver integrates with GitHub Actions, posting detailed markdown summary comments directly on developer pull requests showing metric changes.

A telemetry API records production prompt invocations and user feedback ratings, automatically identifying underperforming production examples to add to future golden test suites.""",
        "data_flow": """The data flow begins when an engineer commits a change to a prompt template or agent tool schema in Git, triggering a GitHub Actions workflow.

The CI runner calls the Evaluation Platform API, passing the updated prompt definitions and the target test suite tag.

The Evaluation Orchestrator spins up parallel worker tasks that retrieve test cases from the database and dispatch prompt requests to Amazon Bedrock endpoints.

As model outputs arrive, automated schema validators check structural validity, while an LLM-as-a-Judge worker evaluates qualitative metrics against established scoring rubrics.

The platform aggregates the scores, computes statistical significance compared to the baseline, updates the pull request status to pass or fail, and archives the run results for historical tracking.""",
        "high_level_design": """At a high level, the architecture features a version-controlled repository, an asynchronous test execution worker pool, an inference gateway, and an analytical reporting layer.

The core service is built with Python and FastAPI, utilizing Celery or AWS SQS with ECS Fargate tasks to distribute parallel inference jobs across multiple worker nodes.

The inference gateway manages rate-limiting, retries, and credential management for foundational models accessible via Amazon Bedrock and internal SageMaker endpoints.

Evaluation results, token usage metrics, and raw model transcripts are persisted in PostgreSQL, with full-text search and embedding comparisons powered by pgvector.

A modern Next.js and React dashboard provides visual analytics, showing historical accuracy trends, latency distributions, and regression alerts across all advertising AI tools.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, mitigating evaluation variance in LLM-as-a-judge pipelines is crucial for reliable CI/CD gates. We accomplish this by configuring the judge model with a temperature of zero and utilizing chain-of-thought grading rubrics that require the judge to output structured reasoning before issuing an integer score.

To keep evaluation fast and cost-effective, the orchestrator implements content-addressable semantic caching: if a test input and prompt template have not changed across commits, the system reuses the cached evaluation output instead of calling the model API again.

To guard against prompt regressions in production, the platform runs shadow evaluations on a small percentage of live production traffic, verifying that the new prompt performs reliably in real-world conditions before a full rollout.

Finally, the platform enforces strict safety guardrails using automated jailbreak and adversarial test batteries, guaranteeing that no prompt modification can bypass corporate brand safety policies or leak internal data."""
    },

    # Q9: Live Commercial Break Prediction & Auto-Cue Signaling System
    {
        "id": 9,
        "title": "Live Event Commercial Break Prediction and Auto-Cue Signaling System",
        "category": "Computer Vision & Broadcast Automation",
        "problem_statement": """Design a predictive AI auto-cue signaling platform that analyzes real-time live sports video, game clock OCR, audio energy, and play-by-play telemetry to predict incoming commercial breaks ten to thirty seconds before they occur. The system must pre-warm ad auctions and prepare SSAI manifest pipelines ahead of unscheduled broadcast timeouts, eliminating latency spikes at the start of breaks.""",
        "clarifying_questions": """To properly design this predictive signaling system, I would first ask about the sports properties we are covering. Sports like football and basketball have structured timeouts, two-minute warnings, and quarter breaks, whereas soccer has continuous forty-five-minute halves with almost no unscheduled breaks. Focusing on football and basketball gives us clear visual and telemetry markers.

Next, I would ask what data sources are available in real time. Do we have access to direct official league data feeds with sub-second latency, or are we solely relying on video frame OCR, commentator audio energy, and referee whistle detection? A multimodal fusion of both official data feeds and video OCR yields the highest reliability.

I would also clarify the tolerance for false positives. If the system predicts an ad break that does not happen, what is the cost? Pre-warming caches has a minor compute cost, but prematurely stitching ads into a live stream would ruin the viewer experience, so predictive signals should only pre-warm auctions, not trigger hard cuts.

Finally, I would ask about the latency budget for the prediction pipeline: the system must process incoming video and telemetry and broadcast the prediction event in under two seconds.""",
        "svg_diagram": generate_svg(
            "Live Commercial Break Prediction Engine",
            [
                ["Live Video & Audio Feed", "Multi-Modal Ingest"],
                ["Game Clock OCR & Audio", "Feature Extractor"],
                ["ML Break Predictor", "Temporal Transformer"],
                ["Pre-Warm Signal Bus", "Redis Pub/Sub"],
                ["SSAI & Auction Fleet", "Pre-Fetched Ad Pods"]
            ]
        ),
        "functional_requirements": """Functionally, the system must ingest the live broadcast feed and apply Optical Character Recognition (OCR) to the scorebug graphics to continuously extract the game clock, shot clock, quarter, and score.

It must simultaneously monitor commentator audio levels and audio frequency signatures to detect sudden drops in crowd noise, referee whistle blasts, and broadcast theme music transitions.

The system must ingest official live sports telemetry APIs, correlating game stoppage events like timeouts, fouls, injuries, and commercial break announcements.

It must feed these multimodal features into a temporal machine learning model to estimate the probability and timing of an impending commercial break within the next thirty seconds.

When the probability exceeds a calibrated threshold, the system must broadcast an Early Ad Warning signal to pre-warm ad auctions and prepare personalized manifests across edge servers.""",
        "non_functional_requirements": """On the non-functional side, prediction latency is critical: the feature extraction and inference pipeline must evaluate conditions continuously with a processing lag of less than one second.

High prediction recall is essential, aiming to anticipate at least ninety-five percent of scheduled and unscheduled commercial breaks ahead of the official SCTE-35 cue.

The system must maintain high resilience, gracefully continuing operation using video OCR alone if upstream official sports telemetry feeds experience network dropouts.

Resource utilization must be optimized to allow the service to monitor dozens of concurrent live games simultaneously without requiring excessive GPU hardware.""",
        "core_entities": """The primary core entity is the Live Game Snapshot, capturing the broadcast identifier, game timestamp, score, remaining quarter time, down and distance, and team timeout counts.

Next is the Audio-Visual Feature Vector, containing extracted audio energy levels, music transition probabilities, referee whistle detections, and clock motion status.

We also have the Break Prediction Event, specifying the predicted break start window, expected break duration, confidence score, and contributing feature signals.

Another entity is the Official Telemetry Event, representing structured play-by-play updates received from sports data partners like Sportradar or Genius Sports.

Finally, the Pre-Warm Command entity defines the instruction sent to downstream ad servers to begin pre-fetching ad pods for viewers assigned to this broadcast.""",
        "api_design": """The system exposes an internal WebSocket and SSE stream called /live/v1/break-predictions, allowing ad servers and manifest engines to subscribe to real-time break probability updates.

There is a low-latency gRPC method named QueryBreakProbability that returns the current prediction score and estimated seconds until the next break on demand.

An administrative REST API enables broadcast operations leads to adjust model confidence thresholds or trigger manual pre-warm signals during high-stakes broadcast moments.

A telemetry ingestion endpoint accepts real-time play-by-play JSON payloads from sports league data providers over persistent HTTP/2 connections.""",
        "data_flow": """The data flow begins when the live broadcast video stream enters an edge ingestion node that extracts audio tracks and crops the scorebug graphic area from incoming frames.

A lightweight OCR pipeline reads the game clock digits every five hundred milliseconds, while an audio signal processor computes spectral noise energy to detect referee whistles and commercial jingles.

Simultaneously, live play-by-play events from the sports data partner arrive via WebSockets, indicating a coach's timeout or television commercial stoppage.

These signals are fused into a feature vector and evaluated by a Temporal Convolutional Network or LSTM model running inference every second.

When the model predicts an ad break with greater than eighty-five percent confidence, it dispatches an Early Warning event to a Redis Pub/Sub channel, prompting the SSAI fleet to initiate background ad auctions twenty seconds before the actual commercial starts.""",
        "high_level_design": """At a high level, the architecture combines computer vision workers, an audio analysis engine, a stream fusion layer, and an event distribution network.

Video frame processing is handled by lightweight C++ workers leveraging OpenCV and optimized Tesseract or custom ONNX OCR models running on CPU-optimized AWS EC2 instances.

Audio analysis runs concurrently using digital signal processing routines to track Root Mean Square energy levels and acoustic pattern fingerprints.

Feature fusion and inference are orchestrated by a Python and FastAPI service utilizing TorchScript models to evaluate state sequences in under fifteen milliseconds.

The output prediction signals are broadcast across global AWS regions using Amazon ElastiCache Redis Pub/Sub, directly notifying regional SSAI and auction workers.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, ensuring rock-solid prediction reliability requires resilient multi-modal sensor fusion. Relying solely on official league data is risky because stadium operators often experience network delays of two to five seconds, whereas relying solely on video OCR can fail if the television network changes its graphic overlay layout mid-season.

Our system solves this by implementing a Bayesian fusion layer that dynamically weights visual OCR, audio spectral features, and official data feeds: if official telemetry drops, the system automatically increases the weight of video clock stoppage and referee whistle detections.

To prevent wasteful compute usage, the prediction signal operates in two distinct stages: a low-confidence threshold of sixty percent triggers background auction pre-fetching for top advertiser tiers, while only the official SCTE-35 cue triggers the actual live video splice.

This ensures that even if an anticipated timeout is canceled or overturned by a challenge, zero incorrect ad insertions occur, yet whenever a break does proceed, the ad pod is already fully calculated and instantly available at the edge."""
    },

    # Q10: Distributed In-Memory Ad Manifest Manipulation Service at CDN Edge
    {
        "id": 10,
        "title": "Distributed In-Memory Ad Manifest Manipulation Service at CDN Edge",
        "category": "Edge Computing & CDN Infrastructure",
        "problem_statement": """Design a globally distributed in-memory manifest manipulation service deployed at the CDN edge using AWS CloudFront and Lambda@Edge. The system must intercept client HLS and DASH manifest requests, look up personalized ad pods from local edge caches, and rewrite live playlists in under ten milliseconds, providing instantaneous response times for millions of concurrent sports viewers.""",
        "clarifying_questions": """To clarify this edge architecture, I would first ask about the computational limits of our edge environment. AWS Lambda@Edge and CloudFront Functions have strict execution time limits and memory constraints, so we need to determine whether playlist manipulation runs within lightweight CloudFront Functions or regional containerized edge points of presence.

Next, I would ask about playlist caching behavior. In live HLS video streaming, client players request a refreshed media playlist every two seconds. Since the underlying video chunks change with every live segment, we need to know whether the manifest manipulation logic is executed on every single poll or if personalized playlists can be short-term cached at the edge.

I would also clarify how personalized ad decisions are propagated to the edge. Does the edge worker pull ad decisions synchronously from a central ad server, or are ad decisions pre-pushed to distributed edge key-value stores like CloudFront KeyValueStore or DynamoDB Global Tables?

Finally, I would ask how the system handles failover if the edge ad cache misses or becomes unavailable during a live broadcast.""",
        "svg_diagram": generate_svg(
            "Edge Manifest Manipulation Service",
            [
                ["Client Video Player", "Polls Playlist (2s)"],
                ["CloudFront Edge Worker", "Lambda@Edge / Envoy"],
                ["Local Edge Cache", "Ad Pod Key-Value Store"],
                ["Manifest Stitcher", "In-Memory Playlist Rewrite"],
                ["Personalized HLS/DASH", "Sub-10ms Response"]
            ]
        ),
        "functional_requirements": """Functionally, the edge manifest service must intercept incoming HTTP GET requests for live HLS m3u8 and DASH mpd playlist files originating from viewers' video players.

The service must parse the client's session cookie or JWT token to extract the viewer's anonymous identifier, device profile, and stream quality level.

It must fetch the baseline live manifest from the origin live video packager and check whether an active SCTE-35 ad break tag is present in the stream.

If an ad break is active, the edge worker must retrieve the pre-computed personalized ad pod for that viewer from its local edge cache and stitch the ad segment URIs into the playlist between EXT-X-DISCONTINUITY tags.

Finally, it must return the customized, valid manifest to the player with appropriate HTTP caching and cross-origin resource sharing headers.""",
        "non_functional_requirements": """From a non-functional perspective, execution latency is the most critical requirement: the entire manifest interception and rewrite must complete in under ten milliseconds at the P99 percentile.

The service must scale linearly to support over twenty million manifest requests per second globally during peak Thursday Night Football commercial breaks.

Availability must be 99.999 percent, ensuring that edge worker errors never cause video stream playback failure for viewers.

Edge memory usage must remain exceptionally compact, fitting all necessary session state and manifest parsing buffers within strict serverless memory limits.""",
        "core_entities": """The primary core entity is the Edge Manifest Request, containing the client IP address, user-agent, requested stream variant, sequence number, and session token.

Next is the Base Live Playlist, representing the raw, un-personalized live video manifest containing the latest camera chunks and SCTE-35 splice markers.

We also have the Edge Cached Ad Pod, which stores the pre-selected ad segment URLs, bitrate variants, duration, and tracking beacon IDs for a specific viewer session.

Another entity is the Edge Manifest Template, providing a pre-parsed memory representation of the playlist to avoid repetitive string parsing.

Finally, the Signed Playback Token entity validates that the client is authorized to stream the requested live sports property.""",
        "api_design": """The service exposes standard HTTP media playlist endpoints such as /live/tnf/variant_1080p.m3u8, which are requested directly by native video player engines.

Internally, edge workers communicate with regional ad decisioning hubs using low-overhead HTTP/2 or gRPC calls to replenish edge ad pod caches ahead of commercial breaks.

There is also an edge invalidation and purge API that allows broadcast operations to instantly update or remove corrupted ad segment URLs across all global edge points of presence.

A lightweight metrics aggregation API emits edge latency histograms, cache hit ratios, and manifest rewrite error counts to Amazon CloudWatch in near real time.""",
        "data_flow": """The data flow begins when a viewer's video player sends a request to the nearest CloudFront edge location to fetch the latest two-second video playlist.

A CloudFront edge worker intercepts the request before it hits the origin cache and retrieves the latest base live manifest generated by AWS Elemental MediaPackage.

The edge worker scans the manifest for ad break cue tags; if none are found, the base manifest is returned immediately to the player.

If an ad cue is detected, the worker queries its local in-memory edge key-value store using the viewer's session ID to retrieve the personalized ad pod segments.

The worker splices the ad segment URLs into the playlist text buffer, adjusts media sequence numbers and discontinuity markers, and delivers the personalized manifest back to the viewer in under seven milliseconds.""",
        "high_level_design": """At a high level, the architecture is distributed across hundreds of global CDN edge points of presence backed by regional origin infrastructure.

The edge layer utilizes AWS CloudFront and Lambda@Edge or regional Envoy proxy nodes running optimized WebAssembly or Rust manifest parsing modules.

Personalized ad decisions are pushed from central ad servers to Amazon CloudFront KeyValueStore and regional ElastiCache clusters ahead of scheduled ad breaks.

Origin live video packagers deliver pristine live HLS and DASH streams into CloudFront origin shield caches, ensuring edge workers always have access to low-latency base manifests.

Edge health monitoring services continuously evaluate manifest delivery latencies, automatically bypassing ad insertion and serving the raw broadcast feed if any edge node exhibits processing delays.""",
        "nfr_deep_dive": """Diving deep into the non-functional requirements, meeting the ultra-fast ten-millisecond execution budget requires avoiding traditional string concatenation and regular expression parsing. Our edge manifest engine is implemented in high-performance Rust compiled to WebAssembly, utilizing zero-copy string slice manipulation to rewrite playlist lines directly in memory buffers.

To prevent edge cache stampedes when millions of viewers request manifests simultaneously, base live manifests are cached at the edge for one second, while personalized ad segments are pre-populated in local edge memory thirty seconds before the commercial break begins.

If an edge worker encounters a cache miss for a viewer's personalized ad pod, it does not hold up the manifest request with a slow synchronous network call. Instead, it immediately falls back to injecting a universal, pre-cached default sponsor ad, maintaining sub-ten-millisecond responsiveness.

All edge workers are stateless and fully isolated: memory buffers are recycled immediately after the HTTP response is written, ensuring stable memory footprints and zero garbage collection pauses during multi-hour live broadcasts."""
    }
]

if __name__ == "__main__":
    print(f"Loaded {len(sysde_questions_part1)} System Design questions (Part 1).")
