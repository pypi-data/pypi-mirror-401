MEMO — Intent Extraction (Explicite vs Implicite) V1.1

Objectif produit

Problème actuel : l’utilisateur formule déjà une décision explicitement dans l’intention (“OAuth avec Clerk”, “Migrer de PostgreSQL vers MongoDB”), mais Preflights redemande la même info en QCM.
Impact : frustration + perte de crédibilité (“l’outil n’écoute pas”).

Règle produit : tout ce qui est explicitement nommé dans l’intention ne doit pas être redemandé.
Donc : on doit distinguer explicit / implicite / absent.
•	Explicite : “OAuth avec Clerk” → pré-remplir et ne pas demander (ou confirmer si ambigu)
•	Implicite : “Ajouter auth” → demander
•	Absent : “token storage”, “session strategy”, “downtime” → demander si pertinent

Ce n’est pas une histoire de “durabilité” d’une décision : c’est une histoire de “assumé + tracé\db vs sous-entendu”.

⸻

Architecture proposée (Hexagonal, propre)

Principe : l’extraction sémantique est un parsing “léger” et déterministe, donc possible en Core.
Mais le filtrage / UX / pré-remplissage appartient à l’Application (orchestrateur).

Pipeline :

Intention (texte)
→ IntentExtractor (Core, pur, déterministe)
→ ExplicitIntent (entities extraites + confidence)
→ QuestionFilter (Application) : supprime questions déjà explicites + produit answers pré-remplies
→ L’UX affiche ce qu’il a détecté (“Detected from your intention: …”) + les questions restantes

⸻

Ajustements essentiels à ton plan (4 points)

1) Ne pas hardcoder le vocabulaire dans le Core

Tu as mis ENTITY_VOCABULARY en dur. Ça recrée exactement le problème “keyword heuristics inside Core”.

Recommandation :
•	Le Core contient l’algorithme d’extraction + la structure ExplicitIntent/ExtractedEntity
•	Le vocabulaire (synonymes, mapping terme → (field_id, normalized_value), seuils) est injecté via HeuristicsConfig (déjà existant)
•	Donc : l’extracteur accepte vocabulary + category mapping en paramètre (ou via config)

Bénéfice : extensible sans changer le Core (langages, stacks, produits).

2) Ajouter une notion de “Policy” : Skip vs Confirm

Il y a des cas où “ne pas demander” est trop agressif.

Ex :
•	“Add auth with JWT” : JWT peut être token type, strategy, session policy…
•	“Use Express” : verbe vs framework
•	“Mongo” : DB ou driver mention

Proposition :
•	Si confidence ≥ 0.9 : auto-fill + skip la question
•	Si 0.75 ≤ confidence < 0.9 : auto-fill mais la question devient une confirmation rapide (pré-sélectionnée)
•	Si < 0.75 : ne rien auto-fill

Cela préserve la crédibilité et évite les faux positifs.

3) Conflits : la réponse utilisateur écrase toujours l’extraction

Priorité :
User answer > explicit intent extraction > defaults/options

Donc :
•	si l’utilisateur répond quelque chose de différent, on remplace
•	on garde une trace “source=intent_extraction” seulement si non écrasé

4) Tracer l’explicite comme “assumé”

Tu veux explicite vs implicite : il faut que ce soit visible dans le flow.

UX : afficher après start :

Detected from your intention:
•	Database target: MongoDB
•	Database source: PostgreSQL

Remaining questions:
•	Migration strategy?
•	Downtime acceptable?

Ce feedback est crucial : l’utilisateur voit que Preflights a compris, et que les questions restantes sont légitimes.

⸻

Modèle de données (recommandé)

Ajouter au Core types :
•	ExtractedEntity
field_id
value
confidence
source_span (start,end)
raw_match (optionnel, utile debug)
normalized_from (optionnel : le terme trouvé)
•	ExplicitIntent
raw_text
entities (tuple)
detected_category (optionnel)
helper get_explicit_value(field_id, min_confidence=0.9)

Côté Application :
•	QuestionFilter retourne
remaining_questions
prefilled_answers
confirmations (optionnel si tu implémentes le mode “confirm”)

⸻

Où l’intégrer (concret)

Dans PreflightsApp.start_preflight :
1.	explicit_intent = IntentExtractor.extract(intention, heuristics_config)
2.	questions = llm_adapter.generate_questions(…) ou templates
3.	(remaining, prefilled) = filter_questions(questions, explicit_intent)
4.	stocker dans session :
•	asked_questions = remaining (ou toutes si tu veux tracer)
•	answers = prefilled (seed)
•	explicit_intent = explicit_intent (optionnel, debug/telemetry)
5.	retourner uniquement remaining_questions

Dans le mode CLI interactif :
•	afficher la section “Detected from your intention” avant la première question (si prefilled non vide)

Dans continue_preflight :
•	rien à changer : answers_delta merge déjà. Les préfilled sont dans session.answers.

⸻

Tests à ajouter (minimum)
1.	test_core_intent_extractor_basic
Intention: “Add OAuth auth with Clerk”
Expect: auth_strategy=OAuth (high confidence), auth_library=Clerk (high confidence), detected_category=Authentication
2.	test_application_question_filter_skips_explicit
Questions: auth_strategy?, auth_library?, oauth_providers?
ExplicitIntent: auth_strategy=OAuth, auth_library=Clerk
Expect: remaining=[oauth_providers], prefilled=[auth_strategy, auth_library]
3.	test_user_answer_overrides_prefill
Prefilled auth_library=Clerk
User answers auth_library=Auth0
Expect final answers auth_library=Auth0
4.	test_ambiguous_term_confirm_policy (si tu fais confirm)
Intention: “Use JWT”
Expect: confidence medium, question turned into confirm not skipped (ou pas prefilled)

⸻

Résultat attendu (exemple UX)

Input :
“Ajouter authentification OAuth avec Clerk”

Output :
Detected from your intention:
•	Strategy: OAuth
•	Library: Clerk

Questions remaining:
•	Which OAuth providers? (Google, GitHub, …, Other)

⸻
