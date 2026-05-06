# Data Acquisition and Ontology Mapping

## 1. Purpose

This document defines the Phase 2 data acquisition and mapping strategy for IIoT-PMO v2. It complements [specification.md](specification.md), [research_review.md](research_review.md), and the v2 ontology artifact [../ontology/iiot-pmo-v2.ttl](../ontology/iiot-pmo-v2.ttl).

The objective is to connect raw industrial sensor records and simulated factory logs to ontology classes in a reproducible way. The mapping strategy is intentionally explicit so that CSV fields, log fields, ontology classes, object properties, and datatype properties can be reviewed by both data scientists and knowledge engineers.

## 2. Data Sources

### 2.1 Industrial Sensor Dataset (Kaggle)

The first source is an industrial sensor dataset obtained from Kaggle. This dataset represents structured time-series data collected from machines or industrial assets. The expected fields include:

| Field | Description | Example |
| --- | --- | --- |
| `timestamp` | Time at which the sensor reading was recorded | `2026-05-06T09:15:00+03:00` |
| `machine_id` | Identifier of the monitored machine | `Motor-01` |
| `sensor_id` | Identifier of the sensor device | `VIB-01` |
| `temp_c` | Temperature in Celsius | `82.4` |
| `vibration_mm_s` | Vibration velocity in mm/s RMS | `8.7` |
| `pressure_bar` | Pressure value in bar | `5.2` |
| `failure_label` | Optional supervised learning label | `bearing_wear` |

Before use, the exact Kaggle dataset license, schema, and citation requirements must be verified. If the selected dataset uses different column names, the staging schema should normalize them to the canonical fields above.

### 2.2 Factory Log Simulation

The second source is a synthetic **Factory Log Simulation**. This source is used to represent realistic maintenance and operations text without exposing confidential plant data. The logs simulate operator notes, maintenance records, alarm narratives, and inspection comments from a large-scale polyester production facility.

The expected fields are:

| Field | Description | Example |
| --- | --- | --- |
| `log_id` | Unique log identifier | `LOG-20260506-001` |
| `timestamp` | Log creation time | `2026-05-06T08:30:00+03:00` |
| `machine_id` | Related machine identifier | `Motor-01` |
| `severity` | Operational severity | `critical` |
| `log_text` | Unstructured maintenance or operator text | `Abnormal vibration observed on Motor-01; bearing inspection requested.` |
| `action_taken` | Maintenance action if available | `bearing inspection` |

The simulated log source supports the LLM-based ontology population strategy described in [research_review.md](research_review.md). The LLM extracts candidate assets, maintenance actions, symptoms, and failure modes from the `log_text` field.

## 3. Acquisition Workflow

```text
Kaggle sensor CSV                         Simulated factory logs
        |                                         |
        v                                         v
Schema normalization                     Text cleaning
        |                                         |
        v                                         v
Time-series validation                   LLM candidate extraction
        |                                         |
        +------------------+----------------------+
                           |
                           v
                 Ontology mapping layer
                           |
                           v
                  RDF/Turtle generation
                           |
                           v
                 IIoT-PMO knowledge graph
```

## 4. Required Mapping Rules

The following mappings satisfy the mandatory Phase 2 requirements:

| Source field | Source type | Ontology target | Mapping rule |
| --- | --- | --- | --- |
| `machine_id` | CSV/log identifier | `iiot:Asset` | Create or reuse an asset individual with URI `iiot:{machine_id}` |
| `temp_c` | Numeric CSV value | `iiot:MeasurementValue` | Create a measurement value individual with `iiot:hasValue` and Celsius unit |

### 4.1 `machine_id` to `Asset`

Each unique `machine_id` is mapped to an ontology individual typed as `iiot:Asset`. If a machine type is known, the individual should also be typed more specifically as `iiot:Motor`, `iiot:Pump`, or another equipment subclass.

Example RDF pattern:

```turtle
iiot:Motor-01
    a iiot:Motor ;
    rdfs:label "Motor-01"@en .
```

### 4.2 `temp_c` to `MeasurementValue`

Each `temp_c` value is mapped to an individual of `iiot:MeasurementValue`. The numeric value is stored with `iiot:hasValue`, and the unit is stored with `iiot:hasUnit`.

Example RDF pattern:

```turtle
iiot:MeasurementValue-Temp-001
    a iiot:MeasurementValue ;
    iiot:hasValue "82.4"^^xsd:decimal ;
    iiot:hasUnit "degC" .
```

The measurement value is then connected to an observation:

```turtle
iiot:Observation-Temp-001
    a iiot:Observation ;
    iiot:hasTimestamp "2026-05-06T09:15:00+03:00"^^xsd:dateTime ;
    iiot:hasMeasurement iiot:MeasurementValue-Temp-001 .
```

## 5. Extended Mapping Table

| Source field | Ontology class | Ontology property | Transformation |
| --- | --- | --- | --- |
| `machine_id` | `iiot:Asset`, `iiot:Equipment` | `rdfs:label` | Normalize identifiers to URI-safe form |
| `sensor_id` | `iiot:Sensor` | `iiot:monitors` | Link sensor to the corresponding equipment |
| `timestamp` | `iiot:Observation` | `iiot:hasTimestamp` | Convert to `xsd:dateTime` |
| `temp_c` | `iiot:MeasurementValue` | `iiot:hasValue`, `iiot:hasUnit` | Decimal value with unit `degC` |
| `vibration_mm_s` | `iiot:MeasurementValue` | `iiot:hasValue`, `iiot:hasUnit` | Decimal value with unit `mm/s RMS` |
| `pressure_bar` | `iiot:MeasurementValue` | `iiot:hasValue`, `iiot:hasUnit` | Decimal value with unit `bar` |
| `failure_label` | `iiot:FailureMode` | `iiot:indicatesFailureMode` | Normalize label to controlled vocabulary |
| `log_text` | `iiot:MaintenanceLog` | `iiot:hasLogText` | Preserve raw evidence text |
| `action_taken` | `iiot:MaintenanceLog` | `iiot:hasMaintenanceAction` | Normalize maintenance action phrase |

## 6. Example Staging Record

```csv
timestamp,machine_id,sensor_id,temp_c,vibration_mm_s,pressure_bar,failure_label
2026-05-06T09:15:00+03:00,Motor-01,VIB-01,82.4,8.7,5.2,bearing_wear
```

This row produces:

- one equipment individual: `iiot:Motor-01`,
- one or more sensor individuals,
- one observation individual per timestamped reading,
- one or more `MeasurementValue` individuals,
- optionally one `FailureMode` individual or relation if `failure_label` is present.

## 7. Example Factory-Style Log

```json
{
  "log_id": "LOG-20260506-001",
  "timestamp": "2026-05-06T08:30:00+03:00",
  "machine_id": "Motor-01",
  "severity": "critical",
  "log_text": "Abnormal vibration observed on Motor-01; bearing inspection requested.",
  "action_taken": "bearing inspection"
}
```

The LLM extraction component should identify:

- `Motor-01` as an `Asset`,
- `abnormal vibration` as evidence related to a vibration condition,
- `bearing inspection` as a maintenance action,
- possible `BearingWear` as a candidate `FailureMode`.

## 8. Data Quality Controls

The ingestion pipeline must apply the following controls before ontology population:

| Control | Rationale |
| --- | --- |
| Timestamp validation | Required for time-series batching and GRU-RNN input |
| Unit normalization | Prevents mixed Celsius/Fahrenheit or pressure-unit errors |
| Identifier normalization | Prevents duplicate assets such as `Motor 01`, `MTR-01`, and `Motor-01` |
| Missing-value handling | Prevents invalid measurements from entering the graph |
| Outlier flagging | Separates plausible faults from sensor corruption |
| Human approval for new classes | Protects ontology schema quality |

## 9. Output Artifacts

The acquisition layer should produce:

- normalized CSV files for machine learning,
- JSON extraction records from the LLM,
- RDF triples conforming to IIoT-PMO v2,
- audit logs linking generated triples to source rows or source text,
- validation reports showing rejected or ambiguous mappings.
