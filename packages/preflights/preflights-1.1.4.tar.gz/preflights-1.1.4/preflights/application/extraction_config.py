"""
Intent Extraction Configuration.

Default vocabulary and thresholds for intent extraction.
These defaults live in Application layer (not Core) and can be overridden.
"""

from __future__ import annotations

from dataclasses import dataclass

from preflights.core.intent_extractor import EntityVocabulary, FieldCategoryMapping


@dataclass(frozen=True)
class ExtractionConfig:
    """Configuration for intent extraction."""

    vocabulary: EntityVocabulary
    field_categories: FieldCategoryMapping
    skip_threshold: float = 0.9  # confidence >= this -> auto-fill + skip question


def default_extraction_config() -> ExtractionConfig:
    """
    Return default V1 extraction configuration.

    Vocabulary maps common terms to (field_id, normalized_value).
    Field IDs are aligned with question IDs from clarifier.py.
    """
    return ExtractionConfig(
        vocabulary=DEFAULT_VOCABULARY,
        field_categories=DEFAULT_FIELD_CATEGORIES,
        skip_threshold=0.9,
    )


# =============================================================================
# DEFAULT VOCABULARY
# =============================================================================
# Format: (term, (field_id, normalized_value))
# Terms are matched case-insensitively
#
# Field IDs aligned with clarifier.py question IDs:
#   auth_strategy, auth_library, oauth_providers
#   db_type, db_orm
#   frontend_framework, styling
#   backend_language, api_style
#   hosting, caching

DEFAULT_VOCABULARY: EntityVocabulary = (
    # ==========================================================================
    # AUTHENTICATION STRATEGY (field_id: auth_strategy)
    # ==========================================================================
    ("oauth2", ("auth_strategy", "OAuth")),
    ("oauth", ("auth_strategy", "OAuth")),
    ("jwt token", ("auth_strategy", "JWT")),
    ("jwt auth", ("auth_strategy", "JWT")),
    # "jwt" alone is ambiguous (could be token format, not strategy) - lower confidence via boundaries
    ("jwt", ("auth_strategy", "JWT")),
    ("magic link", ("auth_strategy", "Magic Links")),
    ("magic links", ("auth_strategy", "Magic Links")),
    ("magiclink", ("auth_strategy", "Magic Links")),
    ("email/password", ("auth_strategy", "Email/Password")),
    ("email password", ("auth_strategy", "Email/Password")),
    ("email + password", ("auth_strategy", "Email/Password")),
    ("email & password", ("auth_strategy", "Email/Password")),
    ("email-password", ("auth_strategy", "Email/Password")),
    ("saml", ("auth_strategy", "SAML")),
    ("passwordless", ("auth_strategy", "Passwordless")),
    ("sso", ("auth_strategy", "SSO")),
    # ==========================================================================
    # AUTHENTICATION LIBRARIES (field_id: auth_library)
    # ==========================================================================
    ("clerk", ("auth_library", "Clerk")),
    ("nextauth.js", ("auth_library", "NextAuth.js")),
    ("nextauth", ("auth_library", "NextAuth.js")),
    ("next-auth", ("auth_library", "NextAuth.js")),
    ("next auth", ("auth_library", "NextAuth.js")),
    ("auth.js", ("auth_library", "Auth.js")),
    ("authjs", ("auth_library", "Auth.js")),
    ("auth0", ("auth_library", "Auth0")),
    ("supabase auth", ("auth_library", "Supabase Auth")),
    ("firebase auth", ("auth_library", "Firebase Auth")),
    ("lucia", ("auth_library", "Lucia")),
    ("passport.js", ("auth_library", "Passport.js")),
    ("passportjs", ("auth_library", "Passport.js")),
    # "passport" alone is ambiguous - only match with .js suffix
    ("keycloak", ("auth_library", "Keycloak")),
    # ==========================================================================
    # DATABASE TYPE (field_id: db_type)
    # ==========================================================================
    ("postgresql", ("db_type", "PostgreSQL")),
    ("postgres", ("db_type", "PostgreSQL")),
    ("mysql", ("db_type", "MySQL")),
    ("mariadb", ("db_type", "MariaDB")),
    ("mongodb", ("db_type", "MongoDB")),
    ("mongo db", ("db_type", "MongoDB")),
    # "mongo" alone kept - usually means MongoDB in tech context
    ("mongo", ("db_type", "MongoDB")),
    ("sqlite", ("db_type", "SQLite")),
    ("dynamodb", ("db_type", "DynamoDB")),
    ("cockroachdb", ("db_type", "CockroachDB")),
    ("supabase", ("db_type", "Supabase")),
    ("planetscale", ("db_type", "PlanetScale")),
    ("neon", ("db_type", "Neon")),
    # ==========================================================================
    # ORM / Query Builder (field_id: db_orm)
    # ==========================================================================
    ("prisma", ("db_orm", "Prisma")),
    ("drizzle orm", ("db_orm", "Drizzle")),
    ("drizzle", ("db_orm", "Drizzle")),
    ("typeorm", ("db_orm", "TypeORM")),
    ("sequelize", ("db_orm", "Sequelize")),
    ("sqlalchemy", ("db_orm", "SQLAlchemy")),
    ("knex", ("db_orm", "Knex")),
    ("kysely", ("db_orm", "Kysely")),
    # ==========================================================================
    # CACHING (field_id: caching)
    # ==========================================================================
    ("redis", ("caching", "Redis")),
    ("memcached", ("caching", "Memcached")),
    # ==========================================================================
    # FRONTEND FRAMEWORK (field_id: frontend_framework)
    # ==========================================================================
    ("next.js", ("frontend_framework", "Next.js")),
    ("nextjs", ("frontend_framework", "Next.js")),
    ("react", ("frontend_framework", "React")),
    ("vue.js", ("frontend_framework", "Vue")),
    ("vuejs", ("frontend_framework", "Vue")),
    ("vue", ("frontend_framework", "Vue")),
    ("nuxt.js", ("frontend_framework", "Nuxt")),
    ("nuxtjs", ("frontend_framework", "Nuxt")),
    ("nuxt", ("frontend_framework", "Nuxt")),
    ("svelte", ("frontend_framework", "Svelte")),
    ("sveltekit", ("frontend_framework", "SvelteKit")),
    ("angular", ("frontend_framework", "Angular")),
    ("remix", ("frontend_framework", "Remix")),
    ("astro", ("frontend_framework", "Astro")),
    ("solidjs", ("frontend_framework", "SolidJS")),
    ("solid.js", ("frontend_framework", "SolidJS")),
    # ==========================================================================
    # STYLING (field_id: styling)
    # ==========================================================================
    ("tailwindcss", ("styling", "Tailwind CSS")),
    ("tailwind css", ("styling", "Tailwind CSS")),
    ("tailwind", ("styling", "Tailwind CSS")),
    ("styled-components", ("styling", "Styled Components")),
    ("styled components", ("styling", "Styled Components")),
    ("css modules", ("styling", "CSS Modules")),
    ("css-modules", ("styling", "CSS Modules")),
    ("emotion", ("styling", "Emotion")),
    ("sass", ("styling", "Sass")),
    ("scss", ("styling", "Sass")),
    # ==========================================================================
    # UI LIBRARY (no direct question ID - informational)
    # ==========================================================================
    ("shadcn/ui", ("ui_library", "shadcn/ui")),
    ("shadcn", ("ui_library", "shadcn/ui")),
    ("radix ui", ("ui_library", "Radix UI")),
    ("radix", ("ui_library", "Radix UI")),
    ("chakra ui", ("ui_library", "Chakra UI")),
    ("chakra", ("ui_library", "Chakra UI")),
    ("material ui", ("ui_library", "Material UI")),
    ("mui", ("ui_library", "Material UI")),
    ("ant design", ("ui_library", "Ant Design")),
    ("antd", ("ui_library", "Ant Design")),
    ("mantine", ("ui_library", "Mantine")),
    # ==========================================================================
    # BACKEND FRAMEWORK (field_id: backend_language includes framework context)
    # ==========================================================================
    ("fastapi", ("backend_framework", "FastAPI")),
    ("express.js", ("backend_framework", "Express")),
    ("expressjs", ("backend_framework", "Express")),
    # "express" alone is ambiguous in English - require .js or js suffix
    ("nestjs", ("backend_framework", "NestJS")),
    ("nest.js", ("backend_framework", "NestJS")),
    ("django", ("backend_framework", "Django")),
    ("flask", ("backend_framework", "Flask")),
    ("hono", ("backend_framework", "Hono")),
    ("elysia", ("backend_framework", "Elysia")),
    ("ruby on rails", ("backend_framework", "Rails")),
    ("rails", ("backend_framework", "Rails")),
    ("laravel", ("backend_framework", "Laravel")),
    ("spring boot", ("backend_framework", "Spring Boot")),
    ("springboot", ("backend_framework", "Spring Boot")),
    # "spring" alone is too ambiguous (season, verb)
    # ==========================================================================
    # API STYLE (field_id: api_style)
    # ==========================================================================
    ("rest api", ("api_style", "REST")),
    ("restful api", ("api_style", "REST")),
    ("restful", ("api_style", "REST")),
    ("graphql", ("api_style", "GraphQL")),
    ("grpc", ("api_style", "gRPC")),
    ("trpc", ("api_style", "tRPC")),
    # ==========================================================================
    # HOSTING (field_id: hosting)
    # ==========================================================================
    ("vercel", ("hosting", "Vercel")),
    ("netlify", ("hosting", "Netlify")),
    ("railway", ("hosting", "Railway")),
    ("fly.io", ("hosting", "Fly.io")),
    ("render", ("hosting", "Render")),
    ("heroku", ("hosting", "Heroku")),
    # Cloud providers - keep but they're often context, not decisions
    # These will only skip if confidence is high (clear word boundaries)
    ("aws", ("hosting", "AWS")),
    ("gcp", ("hosting", "GCP")),
    ("google cloud", ("hosting", "GCP")),
    ("azure", ("hosting", "Azure")),
    # ==========================================================================
    # STATE MANAGEMENT (informational - no direct question ID)
    # ==========================================================================
    ("zustand", ("state_management", "Zustand")),
    ("redux", ("state_management", "Redux")),
    ("jotai", ("state_management", "Jotai")),
    ("recoil", ("state_management", "Recoil")),
    ("mobx", ("state_management", "MobX")),
    ("tanstack query", ("state_management", "TanStack Query")),
    ("react query", ("state_management", "TanStack Query")),
)


# =============================================================================
# FIELD TO CATEGORY MAPPING
# =============================================================================
# Maps field_id to its category for dominant category detection
# Aligned with schema categories: Authentication, Database, Frontend, Backend, Infra

DEFAULT_FIELD_CATEGORIES: FieldCategoryMapping = (
    # Authentication
    ("auth_strategy", "Authentication"),
    ("auth_library", "Authentication"),
    ("oauth_providers", "Authentication"),
    # Database
    ("db_type", "Database"),
    ("db_orm", "Database"),
    ("caching", "Database"),  # Caching often DB-related
    # Frontend
    ("frontend_framework", "Frontend"),
    ("styling", "Frontend"),
    ("ui_library", "Frontend"),
    ("state_management", "Frontend"),
    # Backend
    ("backend_framework", "Backend"),
    ("backend_language", "Backend"),
    ("api_style", "Backend"),
    # Infra
    ("hosting", "Infra"),
)
