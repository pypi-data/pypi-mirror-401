# Locations Where Cypher Queries Are Generated in `src/bento_meta`

## Summary
This document lists all locations in the `python/src/bento_meta` package where Cypher queries are constructed or executed, including file names, function/method context, and line numbers.

---

## `object_map.py`
- `get_q`: 214–221 — MATCH … RETURN
- `get_by_id_q`: 223–227 — MATCH … RETURN
- `get_by_node_nanoid_q`: 229–233 — MATCH … RETURN
- `get_attr_q`: 235–276 — MATCH … RETURN (node/rel variants, LIMIT for object)
- `get_owners_q`: 278–286 — MATCH … RETURN TYPE(r), a
- `put_q`: 288–331 (update with SET/REMOVE) and 335–353 (CREATE … RETURN)
- `put_attr_q` (properties): 366–389 — MATCH … SET … RETURN id(n)
- `put_attr_q` (relationships): 398–418, 421–533 — MATCH … MERGE … RETURN id(a)
- `rm_q`: 540–552 — MATCH … DELETE/DETACH DELETE
- `rm_attr_q` (properties): 560–567 — MATCH … REMOVE … RETURN
- `rm_attr_q` (relationships): 571–639 — MATCH … DELETE r … RETURN

## `model.py`
- `dget`: 460–465 — session.run("match p = … return p")
- `dget`: 480–486 — session.run("match (n:node)-[:has_property]->(p:property) …")
- `dget`: 497–504 — session.run("match (r:relationship)-[:has_property]->(p:property) …")
- `dput` detach cleanup: 553–558 — session.run("match (e)-[r]-() where id(e)=$eid delete r …")

## `mdb/mdb.py`
- `get_model_info`: 167 — "match (m:model) return m"
- `get_model_nodes` (assembled string): 233 — f"match (n:node) {cond} return n"
- `get_model_nodes_edges`: 262–266 — "match p = (s:node)… return p as path"
- `get_node_edges_by_node_id`: 276–283 — match/optional match … return …
- `get_node_and_props_by_node_id`: 292–299 — match/optional match … return …
- `get_nodes_and_props_by_model`: 329–333 — match (n:node)-[:has_property]->(p:property) … return …
- `get_prop_node_and_domain_by_prop_id`: 344–351 — match/optional match … return …
- `get_valueset_by_id`: 362–366 — match … with … match … return …
- `get_valuesets_by_model`: 396–400 — match (vs:value_set)<-[:has_value_set]-(p:property) … return …
- `get_term_by_id`: 409–413 — match/optional match … return …
- `get_props_and_terms_by_model`: 440–443 — match … return …
- `get_origins`: 453 — "match (o:origin) return o"
- `get_origin_by_id`: 459 — "match (o:origin {nanoid:$oid}) where not exists (o._to) return o"
- `get_tags_for_entity_by_id`: 469–472 — match … with … return …
- `get_tags_and_values`: 488–491 — match … return …
- `get_entities_by_tag`: 506–510 — match … with … match … return …
- `get_with_statement`: 516–528 — passes arbitrary read Cypher through

## `mdb/writeable.py`
- `put_with_statement`: 32–36 — passes arbitrary write Cypher through
- `put_term_with_origin`: 45–55 — match … merge … on create set … return t.nanoid

## `mdb/mdb_tools/mdb_tools.py` (uses Cypher builder to generate queries)
- `_get_entity_count`: 86–101 — Statement(Match, Return(count))
- `_get_pattern_count`: 108–122 — Statement(Match, Return(count))
- `remove_entity_from_mdb`: 186–200 — Statement(Match, DetachDelete)
- `add_entity_to_mdb`: 219–243 — Statement(Merge[ent,(src,dst,links)])
- `get_concept_nanoids_linked_to_entity`: 259–285 — Statement(Match, Return, As)
- `add_relationship_to_mdb`: 305–327 — Statement(Match, Merge(triple))
- `get_entity_nanoid`: 430–447 — Statement(Match/Path, Return)
- `get_term_nanoids`: 462–484 — Statement(Match, Return)
- `get_predicate_nanoids`: 496–518 — Statement(Match, Return)
- `get_relationship_between_entities`: 520–542 — Statement(Match, Return TYPE)
- `_get_all_terms`: 556–566 — Statement(Match(term), Return(term.var))
- `get_property_synonyms_direct`: 691–715 — Statement(Match, With/Collect/Return)
- `_get_property_parents_data`: 731–752 — Statement(Match/OptionalMatch/With/Collect/Return)

## `mdb/loaders.py` (generates Cypher via builder for full model loads)
- `load_model`: 20–27 — executes generated statements
- `load_model_statements`: 29–121 — creates Merge/Match/Create/Remove Statements for nodes/edges/props/tags/concepts/terms
- `_cEntity`: 125–177 — builds node property sets for statements
- `_tag_statements`: 183–199 — Statement(Match, Merge has_tag)
- `_prop_statements`: 206–233 — Statement(Merge prop, Match, Merge has_property)
- `_annotate_statements`: 239–273 — Statement chains for concepts/terms/annotations

## `util/cypher/clauses.py` (core Cypher clause generation; string Templates)
- Match: 45
- With: 87
- Create: 96
- Merge: 109
- Remove: 122
- Set/OnCreateSet/OnMatchSet: 147, 173, 183
- Return: 193
- OptionalMatch: 202
- Delete: 242
- DetachDelete: 251
- Statement string assembly and params extraction: 303–341

## `util/_engine.py` (query builder that produces Statement objects and params)
- Statement construction in _create_statement: 227–265
- Walk/parsing that builds patterns and conditions: 269–395

## `util/makeq.py`
- Query.statement and __str__: 57–74 — returns built Statement and string form
- Query.load_paths/set_paths: 34–55 — initializes path-driven query generation

## `util/cypher/entities.py` (pattern text for nodes/relationships that feed into clauses)
- N.pattern/Return: 36–58, 60–67
- R.pattern/Return: 75–99, 101–108
- VarLenR.pattern: 117–147

---

### Notes
- Direct, literal Cypher strings mostly occur in `object_map.py`, `model.py`, `mdb.py`, and `writeable.py`.
- High-level query generation via the clause/statement builder is in `util/cypher/*`, `mdb/loaders.py`, and `mdb_tools/mdb_tools.py`; these ultimately produce Cypher text at runtime via `str(Statement(...))`.
