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
| RDFLib | Optional Python-based parsing and validation |
| FastAPI | Planned backend layer for data ingestion and LLM extraction |
| Ollama/GPT | Planned LLM providers for ontology population |
| GRU-RNN | Planned time-series model for predicted failure generation |

## Repository Structure

```text
.
├── README.md
├── docs
│   ├── data_acquisition.md
│   ├── orsd.docx
│   ├── research_review.md
│   └── specification.md
└── ontology
    ├── iiot-pmo.ttl
    └── iiot-pmo-v2.ttl
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
| Example individuals | Complete | `Motor-01` and `VibrationSensor-01` included |
| Phase 2 ontology | Complete | `MaintenanceLog`, `PredictedFailure`, `TimeSeriesBatch`, `MLModel`, `MeasurementValue` |
| Research review | Complete | LLM ontology population and GRU-RNN article adaptation documented |
| Data acquisition mapping | Complete | Kaggle sensor data and factory log simulation mapping documented |
| LLM ingestion backend | Designed | FastAPI/Ollama/GPT integration plan specified |
| SPARQL query library | Planned | Future validation queries for v2 competency questions |
| Reasoner validation | Planned | Protege/HermiT or Pellet consistency checks |
| External ontology alignment | Planned | SOSA/SSN and maintenance standards alignment |

## Getting Started

Open [ontology/iiot-pmo-v2.ttl](ontology/iiot-pmo-v2.ttl) in Protege to inspect the current ontology. The v1 baseline remains available at [ontology/iiot-pmo.ttl](ontology/iiot-pmo.ttl).

Recommended next validation steps:

1. Load the ontology in Protege.
2. Run a reasoner to check class consistency.
3. Create SPARQL queries from the competency questions in [docs/specification.md](docs/specification.md).
4. Test the data mappings in [docs/data_acquisition.md](docs/data_acquisition.md).
5. Use [docs/research_review.md](docs/research_review.md) as the research basis for LLM ontology population and GRU-RNN adaptation.

## Academic Context

This repository was prepared as a semester project foundation for a Knowledge Engineering and Ontologies course. It follows ontology engineering best practices by starting from an Ontology Requirements Specification Document, then implementing an initial OWL/Turtle model aligned with clearly defined competency questions.
