# 🧬 Trace System

## Purpose

Track each request

---

## Format

trace_id = UUIDv4

---

## Flow

Request → trace_id created  
All layers attach trace_id  
Final response returns trace_id

---

## Rule

Every request MUST have trace_id
