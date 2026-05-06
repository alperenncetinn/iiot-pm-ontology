# Phase 2 Research Review

## 1. Selected Research Integration: Ontology Population Using LLMs

IIoT-PMO v2 adopts **Ontology Population using Large Language Models** as its primary research integration direction. This choice is motivated by the practical impossibility of manually processing large-scale industrial factory data, especially in a large-scale production environment where maintenance logs, operator notes, alarm descriptions, sensor tags, shift reports, and incident narratives are generated continuously.

In such environments, only part of the operational knowledge is available as structured time-series data. A significant portion remains in semi-structured or unstructured textual sources such as maintenance descriptions, alarm explanations, inspection notes, and technician comments. LLMs are suitable for this layer because they can extract candidate assets, sensors, fault symptoms, maintenance actions, temporal expressions, and failure-mode mentions from natural language. These extracted candidates can then be normalized against IIoT-PMO classes and properties before being admitted into the knowledge graph.

This direction is aligned with recent ontology-learning research, where LLMs are evaluated for term typing, taxonomy discovery, relation extraction, and ontology instantiation. For IIoT-PMO, the LLM does not replace the ontology engineer; instead, it acts as a controlled semantic extraction component inside the data ingestion workflow.

## 2. FastAPI-Based Data Ingestion Integration

The proposed implementation places LLM-assisted ontology population inside the **Data Ingestion** layer of the IIoT-PMO architecture.

```text
Industrial data sources
        |
        v
FastAPI ingestion endpoints
        |
        v
Preprocessing and normalization
        |
        v
LLM extraction service: Ollama or GPT
        |
        v
Ontology mapping and validation
        |
        v
RDF triple generation
        |
        v
IIoT-PMO knowledge graph
```

### 2.1 Backend Components

| Component | Responsibility |
| --- | --- |
| `POST /ingest/sensor-csv` | Accepts structured industrial sensor datasets and maps columns to ontology classes |
| `POST /ingest/factory-log` | Accepts simulated factory logs and operator notes |
| `POST /llm/extract-ontology-candidates` | Sends unstructured text to an LLM for entity and relation extraction |
| `POST /kg/populate` | Converts validated extraction results into RDF triples |
| `GET /kg/assets/{asset_id}` | Retrieves semantic asset context, including sensors, observations, alerts, and maintenance history |

### 2.2 LLM Extraction Contract

The LLM should return strictly structured JSON, not free-form prose. A recommended extraction schema is:

```json
{
  "assets": [
    {
      "asset_id": "Motor-01",
      "asset_type": "Motor",
      "location": "Polymerization Line A"
    }
  ],
  "sensors": [
    {
      "sensor_id": "VIB-01",
      "sensor_type": "VibrationSensor",
      "monitors": "Motor-01"
    }
  ],
  "maintenance_logs": [
    {
      "asset_id": "Motor-01",
      "timestamp": "2026-05-06T08:30:00+03:00",
      "action": "bearing inspection",
      "log_text": "Operator reported abnormal vibration on Motor-01."
    }
  ],
  "failure_mentions": [
    {
      "asset_id": "Motor-01",
      "candidate_failure_mode": "BearingWear",
      "evidence": "abnormal vibration"
    }
  ]
}
```

### 2.3 Ollama or GPT Integration Strategy

Two implementation modes are proposed:

| Mode | Model provider | Use case |
| --- | --- | --- |
| Local mode | Ollama | Privacy-preserving extraction from internal factory logs |
| Cloud mode | GPT API | Higher-quality extraction when cloud processing is allowed |

In both modes, the FastAPI backend should wrap the LLM call behind a provider-neutral interface:

```text
LLMProvider.extract_ontology_candidates(text, ontology_context) -> ExtractionResult
```

The `ontology_context` parameter should include a compact representation of relevant IIoT-PMO classes and properties, such as `Asset`, `Sensor`, `MaintenanceLog`, `FailureMode`, `hasSensor`, `monitors`, and `hasMaintenanceHistory`. This reduces hallucinated class names and forces the LLM to align extracted entities with the controlled vocabulary.

### 2.4 Governance and Validation

LLM-generated ontology population must be supervised. The proposed validation sequence is:

1. normalize extracted identifiers such as `Motor 01`, `MTR-01`, and `Motor-01`,
2. reject candidates using classes or properties not present in IIoT-PMO,
3. validate timestamps and numeric values,
4. compare extracted asset IDs against known asset registry entries,
5. store confidence scores and source text references,
6. require human approval for new failure modes or new equipment types.

This design preserves the academic distinction between ontology engineering and automatic ontology population: the ontology schema remains curated, while instances and candidate relations can be generated semi-automatically.

## 3. Mandatory Article Analysis

### 3.1 Article Metadata

| Field | Value |
| --- | --- |
| Title | Personalized ontology and deep training tree-based optimal gated recurrent unit-recurrent neural network for prediction of students' behavior |
| Authors | F. Mary Harin Fernandez, T. Venkata Ramana, Mahammad Shabana, V. Kannagi, M. Nalini |
| Venue | Concurrency and Computation: Practice and Experience |
| Citation identifier | 35(1), e7420 |
| DOI | `10.1002/cpe.7420` |

### 3.2 Problem Addressed by the Article

The article addresses personalized behavior prediction in a digital library context. The authors combine a domain ontology, created with the Protege editor, with a deep learning model based on GRU-RNN. The ontology represents digital-library concepts and their relationships, while the learning model predicts student behavior categories from temporal usage patterns.

The central knowledge engineering contribution is the combination of an explicit semantic model with a predictive model. This is relevant to IIoT-PMO because predictive maintenance also requires a bridge between symbolic knowledge and time-dependent numerical evidence.

### 3.3 Methodological Structure

The methodology can be summarized as follows:

| Stage | Article approach | Interpretation |
| --- | --- | --- |
| Domain modeling | Personalized digital library ontology built in Protege | Formal representation of domain concepts |
| Data representation | User behavior data and digital library interactions | Time-dependent behavioral evidence |
| Prediction model | GRU-RNN | Sequential model for temporal pattern learning |
| Optimization | Deep Training Tree and Black Widow Optimization | Weight optimization and mitigation of learning limitations |
| Evaluation | Accuracy, precision, recall, F-score, and loss | Classification-oriented performance assessment |

GRU-RNN is appropriate in this context because student behavior evolves over time. The same student may show different learning patterns depending on previous interactions, frequency of access, and changes in engagement. GRU units are designed to retain useful temporal information while controlling how much prior state is carried forward.

### 3.4 Adaptation to IIoT-PMO

The article's time-series prediction logic can be adapted directly to **machine failure prediction from sensor data**.

| Article domain | IIoT-PMO adaptation |
| --- | --- |
| Student | Industrial asset such as motor or pump |
| Digital library interaction | Sensor observation or maintenance event |
| Behavior style | Predicted failure condition |
| Personalized ontology | IIoT-PMO asset and maintenance ontology |
| GRU-RNN sequence input | Time-series batch of vibration, temperature, pressure, and current values |
| Behavior prediction output | `PredictedFailure` individual linked to a `FailureMode` |

In IIoT-PMO v2, a time-series window is represented as `TimeSeriesBatch`. The GRU-RNN model consumes batches of sensor observations and predicts a future failure state. The prediction is then represented as a `PredictedFailure` individual, linked to the responsible model through `predictedBy` and to the relevant equipment through `hasPredictedFailure`.

### 3.5 Proposed Predictive Maintenance Pipeline

```text
Sensor observations
        |
        v
TimeSeriesBatch construction
        |
        v
Feature engineering
        |
        v
GRU-RNN model
        |
        v
PredictedFailure output
        |
        v
Ontology population in IIoT-PMO v2
```

A practical example is:

1. `Motor-01` generates vibration and temperature observations.
2. Observations are grouped into `TimeSeriesBatch-Motor-01-2026-05-06`.
3. A GRU-RNN model evaluates temporal degradation patterns.
4. The model predicts a bearing-related failure within a 72-hour horizon.
5. The backend creates `PredictedFailure-Motor-01-BearingWear`.
6. The prediction is linked to `Motor-01`, `BearingWear`, and the ML model that generated it.

### 3.6 Evaluation Adaptation

The article uses accuracy, precision, recall, F-score, and loss. For IIoT-PMO, these metrics should be extended with industrial maintenance metrics:

| Metric | Purpose in IIoT-PMO |
| --- | --- |
| Precision | Reduces unnecessary maintenance interventions |
| Recall | Reduces missed failure events |
| F-score | Balances precision and recall in imbalanced failure datasets |
| Prediction lead time | Measures how early a failure can be predicted |
| False alarm rate | Controls alert fatigue in maintenance teams |
| Mean time between failures | Tracks asset-level reliability trends |
| Downtime avoided | Connects prediction quality to operational value |

### 3.7 Critical Assessment

The article is useful for IIoT-PMO because it demonstrates a hybrid architecture where ontology and deep learning support each other. However, the original domain is educational behavior, where temporal patterns are often less safety-critical than industrial asset degradation. In predictive maintenance, data drift, sensor calibration errors, missing values, rare failure labels, and operational context must be handled more rigorously.

The adaptation therefore requires stronger validation, explainability, and traceability. Each predicted failure should preserve links to the input `TimeSeriesBatch`, the model that produced the prediction, the suspected `FailureMode`, and the source observations.

## 4. References

- Fernandez, F. M. H., Ramana, T. V., Shabana, M., Kannagi, V., & Nalini, M. (2023). Personalized ontology and deep training tree-based optimal gated recurrent unit-recurrent neural network for prediction of students' behavior. *Concurrency and Computation: Practice and Experience*, 35(1), e7420. https://doi.org/10.1002/cpe.7420
- Babaei Giglou, H., D'Souza, J., & Auer, S. (2023). LLMs4OL: Large Language Models for Ontology Learning. *The Semantic Web - ISWC 2023*. https://doi.org/10.1007/978-3-031-47240-4_22
- Neuhaus, F. (2023). Ontologies in the era of large language models: A perspective. *Applied Ontology*, 18(4), 399-407. https://doi.org/10.3233/AO-230072
- Ciatto, G., Agiollo, A., & Omicini, A. (2024). Large language models as oracles for instantiating ontologies with domain-specific knowledge. *Knowledge-Based Systems*, 305, 112940. https://doi.org/10.1016/j.knosys.2024.112940
