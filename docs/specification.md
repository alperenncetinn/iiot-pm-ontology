# Ontology Requirements Specification Document

## 1. Ontology Identification

| Field | Description |
| --- | --- |
| Ontology name | Industrial IoT & Predictive Maintenance Ontology |
| Short name | IIoT-PMO |
| Version | 0.1.0 |
| Domain | Industrial IoT, factory automation, predictive maintenance |
| Representation language | OWL 2, RDF, Turtle |
| Primary artifact | `ontology/iiot-pmo.ttl` |

## 2. Purpose

The purpose of IIoT-PMO is to standardize the representation of factory equipment, industrial sensors, measurements, observations, alerts, maintenance events, and failure modes in predictive maintenance processes.

The ontology is intended to support industrial settings where assets such as motors, pumps, and other rotating equipment are continuously monitored by vibration, temperature, pressure, and current sensors. By formally connecting equipment, sensor data, threshold definitions, and failure semantics, IIoT-PMO enables consistent querying, integration, and reasoning over maintenance knowledge graphs.

## 3. Scope

IIoT-PMO focuses on the semantic layer required for predictive maintenance in industrial IoT environments. The initial scope includes:

- asset and equipment categorization,
- sensor attachment and monitored asset relationships,
- time-stamped sensor observations,
- numeric measurements and thresholds,
- alert generation from abnormal observations,
- failure-mode classification,
- basic maintenance-history representation.

The ontology does not attempt to model low-level PLC programs, full production recipes, enterprise asset management workflows, or vendor-specific device protocols in the initial release.

## 4. Intended Users

The intended users of IIoT-PMO are:

- knowledge engineers designing industrial knowledge graphs,
- maintenance engineers analyzing asset health,
- industrial IT teams integrating sensor data platforms,
- data scientists building predictive maintenance models,
- ontology students and researchers studying applied semantic modeling.

## 5. Intended Uses

The ontology is expected to be used for:

- integrating heterogeneous factory sensor data,
- querying equipment health status through SPARQL,
- relating abnormal sensor values to potential failure modes,
- providing semantic context for AI-based predictive maintenance models,
- supporting dashboard-level asset monitoring and root-cause analysis.

## 6. Competency Questions

The following competency questions define the minimum reasoning and query requirements for the ontology:

| ID | Competency question | Expected answer type |
| --- | --- | --- |
| CQ-01 | Which motors have not received maintenance for more than 1000 operating hours? | List of motor assets |
| CQ-02 | Which vibration sensors currently report values above their critical threshold? | List of vibration sensors and observations |
| CQ-03 | Which equipment items generated alerts during the last 24 hours? | List of equipment, alerts, and timestamps |
| CQ-04 | Which sensors monitor Motor-01? | List of sensors |
| CQ-05 | Which observations are associated with a high vibration failure mode? | List of observations and failure modes |
| CQ-06 | Which assets are monitored by more than one sensor type? | List of assets and sensor types |
| CQ-07 | Which alerts were generated from measurements whose values exceeded configured thresholds? | List of alerts, measurements, and threshold values |
| CQ-08 | Which pumps or motors are associated with repeated abnormal temperature observations? | List of equipment and observations |

## 7. Core Concepts and Classification

### 7.1 Asset

An Asset is a physical or logical entity that has operational relevance in an industrial environment. Assets may include production equipment, auxiliary machinery, sensor devices, and other maintainable objects. In IIoT-PMO, Asset is treated as the upper-level class for entities that can be monitored, maintained, or semantically identified in a factory knowledge graph.

### 7.2 Equipment

Equipment is a subclass of Asset representing industrial machinery that performs a production, utility, or support function. Examples include motors, pumps, compressors, conveyors, and similar devices. Equipment is the main target of predictive maintenance analysis because it can have sensors, observations, alerts, and failure modes associated with it.

### 7.3 Sensor

A Sensor is an Asset that observes a physical property of equipment or its surrounding operational context. Sensors may measure vibration, temperature, pressure, current, flow, or other signals. In the ontology, sensors are linked to the equipment they monitor and to the observations they produce.

### 7.4 Measurement

A Measurement is a structured representation of a numeric or categorical value obtained from an observation. It includes values such as vibration amplitude, temperature, pressure, or current. Measurements may be compared with threshold values to determine abnormal operating conditions.

### 7.5 Observation

An Observation is an event-like record produced by a sensor at a specific time. It connects a sensor, a measured value, and a timestamp. Observations provide the temporal evidence required for detecting trends, anomalies, and threshold violations in predictive maintenance processes.

### 7.6 Alert

An Alert is a semantic notification generated when an observation indicates abnormal or risky behavior. Alerts can be threshold-based, trend-based, or model-based. In the initial ontology, alerts are primarily generated from observations whose measurement values exceed defined thresholds.

### 7.7 FailureMode

A FailureMode is a classification of a potential or observed mechanism of equipment degradation. Examples include bearing wear, misalignment, cavitation, overheating, and imbalance. Failure modes provide diagnostic meaning for alerts and observations, allowing raw sensor data to be interpreted as maintenance-relevant knowledge.

## 8. Relationships

| Property | Domain | Range | Meaning |
| --- | --- | --- | --- |
| `hasSensor` | Equipment | Sensor | Connects equipment to an installed or associated sensor |
| `monitors` | Sensor | Equipment | Indicates which equipment a sensor observes |
| `hasObservation` | Sensor | Observation | Links a sensor to an observation it produced |
| `hasMeasurement` | Observation | Measurement | Connects an observation to its measured value object |
| `generatesAlert` | Observation | Alert | Indicates that an observation generated an alert |
| `indicatesFailureMode` | Alert | FailureMode | Links an alert to a suspected failure mode |
| `hasMaintenanceEvent` | Equipment | MaintenanceEvent | Associates equipment with a maintenance action |

## 9. Data Requirements

| Data property | Domain | Range | Meaning |
| --- | --- | --- | --- |
| `hasValue` | Measurement | `xsd:decimal` | Numeric measurement value |
| `hasTimestamp` | Observation, Alert, MaintenanceEvent | `xsd:dateTime` | Time of observation, alert, or maintenance |
| `hasThreshold` | Sensor | `xsd:decimal` | Configured threshold value for a sensor |
| `hasUnit` | Measurement | `xsd:string` | Unit of measurement |
| `hasOperatingHours` | Equipment | `xsd:decimal` | Operating hours since installation or maintenance |

## 10. Non-Functional Requirements

- The ontology must be readable in Protege.
- The ontology must use stable and descriptive URI identifiers.
- The ontology must be serializable in Turtle format.
- Class and property names must follow consistent UpperCamelCase and lowerCamelCase conventions.
- The ontology should support SPARQL-based validation of competency questions.
- The ontology should be extensible toward SOSA/SSN alignment in future versions.

## 11. Reuse and Alignment Strategy

The initial version is intentionally self-contained for classroom readability and fast inspection in Protege. Future versions should consider alignment with:

- SOSA/SSN for sensor and observation semantics,
- QUDT or OM for measurement units,
- ISO 14224 for equipment reliability and failure data,
- MIMOSA/OpenO&M concepts for asset lifecycle integration.

## 12. Example Scenario

Motor-01 is a production motor monitored by a vibration sensor. The vibration sensor records an observation with a measured vibration value. If the value exceeds the configured threshold, the observation generates a critical alert. The alert may indicate a failure mode such as bearing wear or mechanical imbalance.

This scenario supports the core predictive maintenance workflow: equipment identification, sensor monitoring, observation capture, threshold evaluation, alert generation, and failure-mode interpretation.

## 13. Validation Plan

Validation will be performed by:

1. loading `ontology/iiot-pmo.ttl` in Protege,
2. checking syntax and class hierarchy consistency,
3. writing SPARQL queries for each competency question,
4. adding representative sample individuals for motors, pumps, sensors, observations, and alerts,
5. reviewing the ontology with industrial maintenance and automation domain experts.
