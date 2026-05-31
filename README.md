# Industrial IoT & Predictive Maintenance Ontology (IIoT-PMO)

IIoT-PMO is a lightweight ontology project for standardizing factory equipment, sensor streams, observations, alerts, maintenance history, time-series batches, and predicted failures in industrial predictive maintenance scenarios.

The project is designed for large-scale manufacturing environments such as polyester production plants, where rotating assets, vibration data, temperature trends, threshold-based alerts, and maintenance history must be modeled in a consistent and machine-interpretable way.

## Vision

Modern factories generate enormous volumes of sensor data, yet maintenance teams often struggle with fragmented asset names, inconsistent alarm semantics, and weak links between measurements and failure modes. IIoT-PMO provides a formal vocabulary that connects equipment, sensors, observations, alerts, and predictive maintenance concepts using OWL and RDF.

The long-term goal is to support:

- semantic integration of industrial IoT data,
- SPARQL-based maintenance queries,
- explainable predictive maintenance dashboards,
- LLM-assisted ontology population from factory logs,
- GRU-RNN-based machine failure prediction from sensor time series,
- knowledge graph enrichment for AI and analytics pipelines,
- interoperability with ontology editors such as Protege.

## Technology Stack

| Technology | Role |
| --- | --- |
| OWL 2 | Ontology modeling and formal semantics |
| RDF | Graph-based knowledge representation |
| Turtle | Human-readable ontology serialization |
| SPARQL | Competency-question validation and querying |
| Protege | Ontology editing, inspection, and reasoning |
| RDFLib | Python-based ontology parsing, merging, and serialization |
| Python / Ollama | Local LLM extraction (e.g. gemma4:e2b) for log ingestion |
| GRU-RNN | Time-series prediction framework adapted from academic review |

## Repository Structure

```text
.
├── README.md
├── index.html
├── docs
│   ├── data_acquisition.md
│   ├── orsd.docx
│   ├── research_review.md
│   └── specification.md
├── ontology
│   ├── iiot-pmo.ttl
│   ├── iiot-pmo-v2.ttl
│   ├── sample_individuals.ttl
│   ├── shacl_rules.ttl
│   ├── validation_queries.rq
│   └── populated_data.ttl
└── scripts
    └── populate_ontology.py
```

## Current Scope

IIoT-PMO currently focuses on the core concepts needed for predictive maintenance:

- industrial assets and equipment,
- motor and pump classes,
- vibration, temperature, and pressure sensors,
- sensor observations and numeric measurements,
- threshold-based alerts,
- failure modes and maintenance events,
- maintenance logs and maintenance history,
- time-series batches for predictive modeling,
- predicted failures produced by ML models,
- LLM-assisted extraction from simulated factory logs.

## Progress

| Area | Status | Notes |
| --- | --- | --- |
| Project structure | Complete | `docs/` and `ontology/` directories created |
| ORSD specification | Complete | v2 specification includes version history and Phase 2 scope |
| Core ontology classes | Complete | Asset, Equipment, Sensor, Measurement, Observation, Alert, FailureMode |
| Object properties | Complete | `hasSensor`, `monitors`, `hasObservation`, `generatesAlert` |
| Data properties | Complete | `hasValue`, `hasTimestamp`, `hasThreshold` |
| Example individuals | Complete | CNC_Machine_1, Conveyor_Belt_2, and baseline individuals populated in `ontology/sample_individuals.ttl` |
| Phase 2 ontology | Complete | `MaintenanceLog`, `PredictedFailure`, `TimeSeriesBatch`, `MLModel`, `MeasurementValue` |
| Research review | Complete | LLM ontology population and GRU-RNN article adaptation documented |
| Data acquisition mapping | Complete | Kaggle sensor data and factory log simulation mapping documented |
| LLM ingestion backend | Complete | Python pipeline `scripts/populate_ontology.py` uses local Ollama `gemma4:e2b` and `rdflib` graph merging |
| SPARQL query library | Complete | 4 advanced queries for monitoring, prediction, risk assessment, and avg metrics in `ontology/validation_queries.rq` |
| SHACL validation rules | Complete | Data quality, cardinality, and confidence constraints implemented in `ontology/shacl_rules.ttl` |
| External ontology alignment | Complete | SOSA/SSN ontology mappings (equivalentClass, subClassOf) added to `ontology/iiot-pmo-v2.ttl` |

## Getting Started

1. Open [ontology/iiot-pmo-v2.ttl](ontology/iiot-pmo-v2.ttl) in Protege to inspect the current ontology.
2. Load [ontology/sample_individuals.ttl](ontology/sample_individuals.ttl) to see instantiated CNC/conveyor machinery, sensors, observations, and prediction individuals.
3. Apply SHACL constraints in [ontology/shacl_rules.ttl](ontology/shacl_rules.ttl) to check data quality.
4. Run the validation queries in [ontology/validation_queries.rq](ontology/validation_queries.rq) using a SPARQL engine.
5. Ingest simulated logs and automatically populate the graph by running the Python LLM pipeline:
   ```bash
   pip install openai rdflib
   python3 scripts/populate_ontology.py
   ```

## Academic Context

This repository was prepared as a semester project foundation for a Knowledge Engineering and Ontologies course. It follows ontology engineering best practices by starting from an Ontology Requirements Specification Document, then implementing an initial OWL/Turtle model aligned with clearly defined competency questions.

## 🌐 Live Ontology Documentation

The auto-generated WIDOCO HTML documentation and interactive visualization of the ontology is available online at:
👉 [https://alperenncetinn.github.io/iiot-pm-ontology/](https://alperenncetinn.github.io/iiot-pm-ontology/)

*Note: The live page redirects automatically to the WIDOCO documentation inside `docs/widoco/`, but allows navigating to the custom Interactive Ontology Console (`console.html`) for dynamic graph exploration.*
