"""LLM prompt templates for intent generation.

This module provides prompt templates for generating structured intents
from user objectives. Prompts guide the LLM to extract or expand objectives
into problem statements, assumptions, requirements, acceptance criteria,
and explicit non-goals.

Project state awareness (FEAT-AUTO-INTENT-002):
    - EMPTY projects get "Foundation Proposals" section with tech recommendations
    - EXISTING projects get "Questions for Derivation" section for investigation

Related:
    - docs/design/briefs/AUTO_INTENT_GENERATION_BRIEF.md
    - docs/design/briefs/AUTO_INTENT_POLISH_BRIEF.md
    - obra/intent/models.py
    - obra/hybrid/handlers/intent.py
"""

from obra.intent.models import InputType


# Lazy import to avoid circular dependency
def _get_project_state():
    from obra.intent.detection import ProjectState  # pylint: disable=C0415
    return ProjectState


def build_intent_generation_prompt(
    objective: str,
    input_type: InputType,
    project_state: str | None = None,
) -> str:
    """Build LLM prompt for intent generation.

    Args:
        objective: User objective or input text
        input_type: Classification of input type
        project_state: Optional project state (EMPTY or EXISTING)

    Returns:
        Formatted prompt string for LLM

    Example:
        >>> prompt = build_intent_generation_prompt("add auth", InputType.VAGUE_NL, "EMPTY")
        >>> # Prompt includes Foundation Proposals section...
    """
    if input_type == InputType.VAGUE_NL:
        return _build_vague_nl_prompt(objective, project_state)
    if input_type == InputType.RICH_NL:
        return _build_rich_nl_prompt(objective, project_state)
    if input_type == InputType.PRD:
        return _build_prd_extraction_prompt(objective, project_state)
    if input_type == InputType.PROSE_PLAN:
        return _build_prose_plan_extraction_prompt(objective, project_state)

    # Fallback to vague NL
    return _build_vague_nl_prompt(objective, project_state)


def _build_vague_nl_prompt(objective: str, project_state: str | None = None) -> str:
    """Build prompt for expanding vague natural language objectives.

    Args:
        objective: Short, underspecified objective
        project_state: Optional project state (EMPTY or EXISTING)

    Returns:
        Prompt template for vague NL expansion
    """
    # Add context-aware section based on project state
    context_section = ""
    if project_state == "EMPTY":
        context_section = """
6. **Foundation Proposals**: Since this is a new/minimal project, propose 3-5 foundational technology choices:
   - Core framework or language (if not specified)
   - Database or data storage approach
   - Key libraries or tools for the objective
   - Deployment or hosting considerations
   Include brief rationale for each proposal.
"""
    elif project_state == "EXISTING":
        context_section = """
6. **Questions for Derivation**: Since this is an existing codebase, list 3-5 questions that need investigation:
   - What is the current technology stack?
   - How is [relevant component] currently implemented?
   - Are there existing patterns or conventions to follow?
   - What dependencies or integrations exist?
   These questions will guide the derivation process.
"""

    yaml_section = ""
    if project_state == "EMPTY":
        yaml_section = """foundation_proposals:
  - "Proposal with rationale"
  - "Second proposal with rationale"
"""
    elif project_state == "EXISTING":
        yaml_section = """derivation_questions:
  - "First investigation question"
  - "Second investigation question"
"""

    return f"""You are an AI assistant helping to clarify and structure a \
software development objective.

The user provided this brief objective:
"{objective}"

Your task is to expand this into a structured intent with the following sections:

1. **Problem Statement**: A clear, detailed description of what the user wants to achieve (2-3 sentences)

   Quality checklist:
   - ✅ States WHAT needs to be solved, not HOW (avoid implementation details)
   - ✅ Quantifies impact where possible (users, frequency, scale)
   - ✅ Identifies the root need or problem
   - ❌ Avoid vague goals ("improve system", "make it better")
   - ❌ Avoid jumping to solutions ("we need to use Redis")

   Example (good): "Users cannot track their order status after checkout, requiring 20+ daily support calls. They need real-time visibility into shipping progress."

   Example (bad): "The system needs improvement."

2. **Assumptions**: List 2-4 reasonable assumptions about:
   - Technology choices (if not specified)
   - User experience expectations
   - Integration requirements
   - Performance/scale considerations

   Quality checklist:
   - ✅ Specific and testable assumptions
   - ✅ Technical context that affects implementation
   - ✅ Reasonable defaults when requirements are underspecified
   - ❌ Avoid vague statements ("system will be fast")
   - ❌ Don't disguise requirements as assumptions

   Example (good): "Assumes email delivery within 60 seconds is acceptable for password reset flow"

   Example (bad): "System will perform well"

3. **Requirements**: List 4-8 specific functional requirements that would satisfy this objective

   Prioritization framework:
   - [MUST HAVE]: Core functionality; objective fails without it
   - [SHOULD HAVE]: Important but objective could succeed without it
   - [COULD HAVE]: Nice to have; enhances solution but not essential

   Format each as: "[PRIORITY] Requirement description"

   Example: "[MUST HAVE] User can create an account with email and password"
   Example: "[SHOULD HAVE] User receives welcome email upon registration"
   Example: "[COULD HAVE] User can upload profile picture during signup"

4. **Constraints**: Capture explicit constraints and inferred boundaries

   Quality checklist:
   - ✅ Include platform, policy, compliance, or environment constraints
   - ✅ Capture time, budget, performance, or tooling limits if implied
   - ❌ Avoid implementation choices unless mandated

   Example (good): "Must comply with internal security review checklist"
   Example (good): "Must run on Linux and macOS"

5. **Acceptance Criteria**: List 3-5 verifiable criteria that indicate successful completion

   Quality checklist:
   - ✅ Measurable and testable (can be verified objectively)
   - ✅ Specific success conditions
   - ✅ Clear pass/fail criteria
   - ❌ Avoid vague statements ("works well", "is user-friendly")
   - ❌ Avoid subjective criteria that can't be tested

   Example (good): "User can reset password and login successfully within 5 minutes of requesting reset"

   Example (bad): "Password reset works well"

6. **Non-Goals**: Explicitly list 2-3 things that are OUT OF SCOPE for this objective

   Scope guidance:
   - Be specific about what's excluded (not just "we won't do everything")
   - Identify logical adjacent features that are tempting but separate
   - Consider what could be "phase 2" vs included in this objective
   - Set realistic boundaries for the objective size

   Example (good): "OAuth social login (Google, GitHub) - will be added separately"
   Example (good): "Admin user management interface - out of scope for MVP"

   Example (bad): "Extra features"
   Example (bad): "Nice-to-have items"
{context_section}
Common mistakes to avoid:

❌ **Vague problem statements**: "Improve the system" doesn't explain WHAT needs solving
❌ **Assumptions disguised as requirements**: Put them in the right section
❌ **Requirements that specify HOW**: Focus on WHAT outcome is needed, not implementation
❌ **Untestable acceptance criteria**: "Should work well" isn't verifiable
❌ **Generic non-goals**: "We won't do everything" isn't specific enough
❌ **Scope creep**: "And also..." usually means you need to split objectives

7. **Risks**: Identify key risks or failure modes to monitor

   Example (good): "Risk of breaking existing OAuth callbacks"
   Example (good): "Risk of long-running migration timing out in prod"

Return your response using YAML frontmatter followed by optional markdown body:

---
problem_statement: "Clear description of the problem..."
assumptions:
  - "First assumption"
  - "Second assumption"
requirements:
  - "First requirement"
  - "Second requirement"
constraints:
  - "First constraint"
  - "Second constraint"
acceptance_criteria:
  - "First criterion"
  - "Second criterion"
non_goals:
  - "First non-goal"
  - "Second non-goal"
risks:
  - "First risk"
  - "Second risk"
{yaml_section}---

# Additional Context (Optional)

You may include additional explanatory notes, diagrams, or clarifications here in markdown format if needed.

Note on structure adaptation:
- These sections provide a framework, not a rigid template
- If assumptions are obvious, keep them brief (2-3 vs 4-6)
- If scope is inherently small, fewer requirements are fine
- Adapt section depth to the objective's complexity
- Quality over completeness: don't pad sections just to fill them

Be specific and concrete. Avoid vague language. Make reasonable assumptions \
when details are missing."""


def _build_rich_nl_prompt(objective: str, project_state: str | None = None) -> str:
    """Build prompt for extracting structure from rich natural language.

    Args:
        objective: Detailed natural language description
        project_state: Optional project state (EMPTY or EXISTING)

    Returns:
        Prompt template for rich NL extraction
    """
    context_section = ""
    if project_state == "EMPTY":
        context_section = """
6. **Foundation Proposals**: Since this is a new/minimal project, propose foundational technology choices based on the objective.
"""
    elif project_state == "EXISTING":
        context_section = """
6. **Questions for Derivation**: Since this is an existing codebase, list questions that need investigation to implement this objective.
"""

    yaml_section = ""
    if project_state == "EMPTY":
        yaml_section = """foundation_proposals:
  - "Proposal with rationale"
"""
    elif project_state == "EXISTING":
        yaml_section = """derivation_questions:
  - "Investigation question"
"""

    return f"""You are an AI assistant helping to structure and enrich a \
software development objective.

The user provided this detailed objective:
"{objective}"

Your task is to extract, expand, and enrich this information into a structured intent with these sections. Remember: EXTRACT what's stated AND ENRICH by inferring implicit requirements, technical assumptions, and quality standards.

1. **Problem Statement**: Extract or synthesize the core problem being solved (2-3 sentences), adding clarity where needed

   Quality checklist:
   - ✅ States WHAT needs to be solved, not HOW (avoid implementation details)
   - ✅ Quantifies impact where possible (users, frequency, scale)
   - ✅ Synthesizes the core need, don't just copy-paste user's words
   - ❌ Avoid vague goals ("improve system", "make it better")
   - ❌ Avoid jumping to solutions ("we need to use Redis")

   Example (good): "Users currently wait 3-5 seconds for dashboard data to load, causing 40% to abandon before viewing. Mobile users on 4G connections are particularly affected. We need to reduce initial load time to under 1 second."

   Example (bad): "The dashboard needs to be faster."

2. **Assumptions**: Identify stated assumptions AND infer reasonable technical assumptions

   Quality checklist:
   - ✅ Extract explicit assumptions from the objective
   - ✅ Infer reasonable technical defaults (versions, encodings, standards)
   - ✅ Consider performance, scale, and error handling expectations
   - ✅ Identify user context or constraints
   - ❌ Avoid vague statements ("system will be fast")
   - ❌ Don't disguise requirements as assumptions

   Categories to consider:
   - Technology versions (e.g., Python 3.12+, Node 18+)
   - Encoding/charset expectations (e.g., UTF-8)
   - Error handling approach
   - Performance/scale assumptions
   - User context or constraints

   Example (good): "Assumes Redis 7.0+ available for caching layer"
   Example (good): "Assumes API response times <200ms acceptable for list endpoints"

   Example (bad): "System will perform well"

3. **Requirements**: Extract explicit requirements AND infer implicit ones

   Prioritization framework:
   - [MUST HAVE]: Core functionality; objective fails without it
   - [SHOULD HAVE]: Important but objective could succeed without it
   - [COULD HAVE]: Nice to have; enhances solution but not essential

   Format each as: "[PRIORITY] Requirement description"

   Extraction + enrichment pattern:
   - What's directly stated in the objective
   - What's implied by the objective (edge cases, error handling)
   - Standard features for this type of system
   - Quality attributes mentioned (performance, security, usability)

   Example (good): "[MUST HAVE] API endpoint returns paginated user list with max 100 items per page"
   Example (good): "[SHOULD HAVE] Email validation includes format check and disposable domain detection"
   Example (good): "[COULD HAVE] User can export search results as CSV"

   Example showing enrichment:
   User says: "Add user registration with email"
   You infer:
   - [MUST HAVE] User can create account with email and password
   - [MUST HAVE] Email verification required before account activation
   - [SHOULD HAVE] Password strength validation (min 8 chars, mixed case, numbers)
   - [COULD HAVE] Prevent registration with disposable email domains

4. **Constraints**: Extract explicit constraints and infer required boundaries

   Quality checklist:
   - ✅ Capture platform, compliance, policy, or environment constraints
   - ✅ Include performance or operational limits implied by the objective
   - ❌ Avoid implementation preferences unless mandated

   Example (good): "Must support Safari and Chrome on macOS"
   Example (good): "Must comply with GDPR data retention policy"

5. **Acceptance Criteria**: Derive verifiable criteria even when not explicitly stated

   Quality checklist:
   - ✅ Measurable and testable (can be verified objectively)
   - ✅ Specific success conditions
   - ✅ Infer quality standards from objective context
   - ✅ Clear pass/fail criteria
   - ❌ Avoid vague statements ("works well", "is user-friendly")
   - ❌ Avoid subjective criteria that can't be tested

   Example (good): "User can complete password reset and login successfully within 5 minutes of requesting reset link"
   Example (good): "API returns search results in under 500ms for 95% of requests"
   Example (good): "Email notification delivered within 60 seconds of trigger event"

   Example (bad): "Password reset works well"
   Example (bad): "System is fast enough"

6. **Non-Goals**: Infer scope boundaries based on the focus

   Scope guidance:
   - Be specific about what's excluded (not just "we won't do everything")
   - Identify logical adjacent features that are tempting but separate
   - Consider what could be "phase 2" vs included in this objective
   - Set realistic boundaries for the objective size

   Example (good): "OAuth social login (Google, GitHub) - will be added in separate feature"
   Example (good): "Admin user management interface - out of scope for MVP"
   Example (good): "Real-time collaboration features - deferred to phase 2"

   Example (bad): "Extra features"
   Example (bad): "Nice-to-have items"
{context_section}
Common mistakes to avoid:

❌ **Just transcribing**: Don't copy-paste the user's words—synthesize and enrich
❌ **Missing implicit requirements**: If user says "add login", infer password reset, session management, etc.
❌ **Vague problem statements**: Add specificity and impact quantification
❌ **Assumptions that are requirements**: Separate what's assumed from what's required
❌ **Untestable acceptance criteria**: "Should work well" isn't verifiable
❌ **Generic non-goals**: "We won't do everything" isn't specific enough

7. **Risks**: Identify key risks or failure modes to watch

   Example (good): "Risk of breaking pagination for existing API clients"
   Example (good): "Risk of compliance review delaying release"

Return your response using YAML frontmatter followed by optional markdown body:

---
problem_statement: "Clear description of the problem..."
assumptions:
  - "First assumption"
  - "Second assumption"
requirements:
  - "[MUST HAVE] First requirement"
  - "[SHOULD HAVE] Second requirement"
constraints:
  - "First constraint"
  - "Second constraint"
acceptance_criteria:
  - "First criterion"
  - "Second criterion"
non_goals:
  - "First non-goal"
  - "Second non-goal"
risks:
  - "First risk"
  - "Second risk"
{yaml_section}---

# Additional Context (Optional)

You may include additional explanatory notes, diagrams, or clarifications here in markdown format if needed.

Note on enrichment:
- Extract explicit information, then expand with reasonable inferences
- Add clarity and structure beyond what's explicitly stated
- Infer implicit requirements, technical assumptions, and quality standards
- Make the intent document more valuable for planning and implementation
- Quality over completeness: don't pad sections just to fill them
- Adapt section depth to the objective's complexity

Be specific and concrete. When expanding on user input, make reasonable \
assumptions explicit rather than leaving them implicit."""


def _build_prd_extraction_prompt(prd_content: str, project_state: str | None = None) -> str:
    """Build prompt for extracting intent from PRD documents.

    Args:
        prd_content: Full PRD document content
        project_state: Optional project state (EMPTY or EXISTING)

    Returns:
        Prompt template for PRD extraction
    """
    context_section = ""
    yaml_section = ""
    if project_state == "EMPTY":
        context_section = """
6. **Foundation Proposals**: Since this is a new/minimal project, propose foundational technology choices based on the PRD requirements.
"""
        yaml_section = """foundation_proposals:
  - "Proposal with rationale"
"""
    elif project_state == "EXISTING":
        context_section = """
6. **Questions for Derivation**: Since this is an existing codebase, list \
questions that need investigation to implement this PRD.
"""
        yaml_section = """derivation_questions:
  - "Investigation question"
"""

    return f"""You are an AI assistant helping to extract a structured intent \
from a Product Requirements Document (PRD).

Below is the PRD content:

---
{prd_content}
---

Your task is to extract the key information and structure it as an intent with these sections:

1. **Problem Statement**: Extract the problem or opportunity from Overview, Background, or Problem Statement sections (2-3 sentences)

   Quality checklist:
   - ✅ Extract WHAT needs to be solved, not HOW (avoid implementation details)
   - ✅ Preserve quantified impact from the PRD (users, revenue, efficiency)
   - ✅ Synthesize from multiple sections if needed (don't just copy first paragraph)
   - ❌ Avoid vague statements if PRD has specifics
   - ❌ Don't extract solution descriptions as the problem

   Example (good): "Customer support team manually processes 200+ refund requests daily, taking 15 minutes each. They need automated refund approval for standard cases to reduce processing time to under 2 minutes."

   Example (bad): "Need to improve the refund system."

   Typical PRD sections to check: Overview, Background, Problem Statement, Executive Summary

2. **Assumptions**: Extract stated assumptions, constraints, and context from the PRD

   Quality checklist:
   - ✅ Extract explicit assumptions from PRD (technical constraints, user context)
   - ✅ Preserve specific versions, standards, or technical requirements
   - ✅ Include performance, scale, or compliance assumptions
   - ❌ Avoid inventing assumptions not in the PRD
   - ❌ Don't extract requirements and label them as assumptions

   Example (good): "Assumes existing payment gateway supports automated refunds via API"
   Example (good): "Assumes refund processing volume <500 requests per day"

   Example (bad): "System will work well"

   Typical PRD sections to check: Assumptions, Constraints, Context, Technical Requirements

3. **Requirements**: Extract all functional requirements and assign priorities

   Prioritization framework:
   - [MUST HAVE]: Core functionality; PRD objective fails without it
   - [SHOULD HAVE]: Important but PRD could succeed without it
   - [COULD HAVE]: Nice to have; enhances solution but not essential

   Format each as: "[PRIORITY] Requirement description"

   Quality checklist:
   - ✅ Extract from Functional Requirements, Features, User Stories sections
   - ✅ Preserve technical specifics (API endpoints, data formats, integration points)
   - ✅ Assign priorities based on PRD emphasis (MVP vs Phase 2, etc.)
   - ✅ Focus on WHAT outcome is needed, not implementation details
   - ❌ Don't extract HOW (implementation architecture) as requirements

   Example (good): "[MUST HAVE] System automatically approves refunds under $50 for orders older than 30 days"
   Example (good): "[SHOULD HAVE] Support staff receive email notification for each automated refund"
   Example (good): "[COULD HAVE] Dashboard shows daily refund processing statistics"

   Typical PRD sections to check: Functional Requirements, Features, User Stories, Capabilities

4. **Constraints**: Extract explicit constraints or boundaries from the PRD

   Quality checklist:
   - ✅ Capture platform, compliance, or legal constraints
   - ✅ Preserve operational limits (performance, uptime, regions)
   - ❌ Avoid implementation choices unless mandated

   Example (good): "Must retain audit logs for 7 years"
   Example (good): "Must support EU and US data residency"

   Typical PRD sections to check: Constraints, Non-Functional Requirements, Compliance

5. **Acceptance Criteria**: Extract success criteria, acceptance tests, or verification methods

   Quality checklist:
   - ✅ Extract measurable criteria (testable, verifiable)
   - ✅ Preserve specific metrics from PRD (response times, accuracy, throughput)
   - ✅ Include test scenarios if provided
   - ❌ Avoid vague criteria if PRD has specifics
   - ❌ Don't extract subjective statements ("works well")

   Example (good): "Automated refund decision completes in under 5 seconds for 95% of requests"
   Example (good): "Manual review queue shows pending requests within 30 seconds of submission"

   Example (bad): "Refund system works properly"

   Typical PRD sections to check: Acceptance Criteria, Success Metrics, Verification, Testing

6. **Non-Goals**: Extract explicitly mentioned out-of-scope items, future work, or non-requirements

   Scope guidance:
   - Extract specific exclusions from the PRD (don't invent them)
   - Look for "Phase 2", "Future Work", "Out of Scope" sections
   - Preserve rationale if provided ("deferred due to..." → "deferred")
   - Be specific about what's excluded

   Example (good): "International refunds (non-USD currencies) - deferred to Phase 2"
   Example (good): "Partial refunds - out of scope for automated processing"

   Example (bad): "Other features"
   Example (bad): "Nice-to-have items"

   Typical PRD sections to check: Non-Goals, Out of Scope, Future Work, Phase 2
{context_section}
Common mistakes to avoid:

❌ **Transcribing HOW instead of WHAT**: Extract the outcome needed, not the implementation approach
❌ **Missing priorities**: PRD often indicates MVP vs Phase 2—use this to assign [MUST HAVE]/[SHOULD HAVE]
❌ **Vague problem statements**: If PRD has metrics or impact, preserve them
❌ **Inventing content**: Extract only what's in the PRD; don't infer beyond what's stated
❌ **Ignoring structure**: PRD sections are intentional—map them to the right intent sections
❌ **Generic non-goals**: Extract specific exclusions, not placeholder text

7. **Risks**: Extract key risks or failure modes stated in the PRD

   Example (good): "Risk: Manual review backlog could exceed SLA during peak season"
   Example (good): "Risk: Dependency on third-party fraud API availability"

Return your response using YAML frontmatter followed by optional markdown body:

---
problem_statement: "Clear description of the problem..."
assumptions:
  - "First assumption"
  - "Second assumption"
requirements:
  - "[MUST HAVE] First requirement"
  - "[SHOULD HAVE] Second requirement"
constraints:
  - "First constraint"
  - "Second constraint"
acceptance_criteria:
  - "First criterion"
  - "Second criterion"
non_goals:
  - "First non-goal"
  - "Second non-goal"
risks:
  - "First risk"
  - "Second risk"
{yaml_section}---

# Additional Context (Optional)

You may include additional explanatory notes, diagrams, or clarifications here in markdown format if needed.

Note on extraction:
- Preserve technical specifics and metrics from the PRD
- Map PRD sections to intent structure (Features → Requirements, \
Success Metrics → Acceptance Criteria)
- Assign priorities based on PRD emphasis (MVP, Phase 1, Critical, etc.)
- Extract WHAT is needed, not HOW it will be built
- If PRD is vague in a section, keep extraction brief rather than inventing content"""


def _build_prose_plan_extraction_prompt(plan_content: str, project_state: str | None = None) -> str:
    """Build prompt for extracting intent from prose plan documents.

    Args:
        plan_content: Full prose plan content
        project_state: Optional project state (EMPTY or EXISTING)

    Returns:
        Prompt template for prose plan extraction
    """
    context_section = ""
    yaml_section = ""
    if project_state == "EMPTY":
        context_section = """
6. **Foundation Proposals**: Since this is a new/minimal project, propose foundational technology choices based on the plan's requirements.
"""
        yaml_section = """foundation_proposals:
  - "Proposal with rationale"
"""
    elif project_state == "EXISTING":
        context_section = """
6. **Questions for Derivation**: Since this is an existing codebase, list \
questions that need investigation to implement this plan.
"""
        yaml_section = """derivation_questions:
  - "Investigation question"
"""

    return f"""You are an AI assistant helping to extract a structured intent \
from an implementation plan document.

Below is the plan content:

---
{plan_content}
---

Your task is to extract the underlying objective and structure it as an intent with these sections:

CRITICAL: Plans describe HOW to implement something. Your job is to extract WHAT needs to be achieved (the intent), not the implementation steps.

1. **Problem Statement**: Synthesize what problem this plan is trying to solve (2-3 sentences)

   Quality checklist:
   - ✅ Extract WHAT outcome is needed, not the implementation approach
   - ✅ Look for objective, goal, or purpose statements in the plan
   - ✅ Synthesize from context if not explicitly stated
   - ✅ Preserve impact or motivation if mentioned
   - ❌ Avoid describing the implementation steps as the problem
   - ❌ Don't extract technical architecture decisions as the problem

   Example (good): "Development team needs to reduce deployment time from 45 minutes to under 10 minutes to enable rapid iteration and hotfix deployments."

   Example (bad): "Need to implement CI/CD pipeline with GitHub Actions."

   Typical plan sections to check: Objective, Goal, Purpose, Background, Motivation

2. **Assumptions**: Extract stated assumptions, prerequisites, or constraints from the plan

   Quality checklist:
   - ✅ Extract explicit assumptions about existing systems or context
   - ✅ Identify prerequisites or dependencies mentioned
   - ✅ Include constraints that affect the approach
   - ❌ Avoid inventing assumptions not in the plan
   - ❌ Don't extract implementation choices as assumptions

   Example (good): "Assumes GitHub Actions available (team has GitHub Enterprise)"
   Example (good): "Assumes Docker registry accessible from deployment environment"

   Example (bad): "Implementation will be successful"

   Typical plan sections to check: Assumptions, Prerequisites, Constraints, Dependencies

3. **Requirements**: Extract the key deliverables or outcomes this plan aims to produce

   Prioritization framework:
   - [MUST HAVE]: Core deliverable; plan objective fails without it
   - [SHOULD HAVE]: Important but plan could succeed without it
   - [COULD HAVE]: Nice to have; enhances solution but not essential

   Format each as: "[PRIORITY] Requirement description"

   Quality checklist:
   - ✅ Extract deliverables (WHAT will be produced), not implementation steps (HOW)
   - ✅ Focus on outcomes, not technical tasks
   - ✅ Look for "deliverables", "outcomes", "goals" sections
   - ✅ Assign priorities based on plan emphasis (MVP, critical, optional)
   - ❌ Don't extract "Step 1: Do X, Step 2: Do Y" as requirements
   - ❌ Avoid technical HOW details ("use React hooks" is implementation, not requirement)

   Example showing WHAT vs HOW:
   Plan says: "Step 1: Create GitHub Actions workflow file. Step 2: Configure Docker build step. Step 3: Add deployment stage."
   You extract: "[MUST HAVE] Automated deployment pipeline that builds and deploys on every push to main branch"

   Example (good): "[MUST HAVE] Deployment completes in under 10 minutes from commit to production"
   Example (good): "[SHOULD HAVE] Failed deployments automatically roll back to previous version"
   Example (good): "[COULD HAVE] Slack notification sent on deployment completion"

   Typical plan sections to check: Goals, Deliverables, Outcomes, Completion Criteria

4. **Constraints**: Extract constraints or boundaries stated in the plan

   Quality checklist:
   - ✅ Capture platform, policy, or environment constraints
   - ✅ Preserve performance, timing, or tooling limits
   - ❌ Avoid implementation choices unless mandatory

   Example (good): "Must deploy within a 10-minute maintenance window"
   Example (good): "Must run within existing Kubernetes cluster limits"

   Typical plan sections to check: Constraints, Assumptions, Dependencies

5. **Acceptance Criteria**: Extract how success will be measured

   Quality checklist:
   - ✅ Extract verification, testing, or completion criteria
   - ✅ Look for measurable success conditions
   - ✅ Preserve specific metrics if provided
   - ❌ Avoid vague criteria ("implementation works")
   - ❌ Don't extract test steps as criteria (extract the pass condition)

   Example (good): "Deployment from commit to production completes in under 10 minutes for 95% of deploys"
   Example (good): "Zero-downtime deployments verified through continuous health checks"

   Example (bad): "Pipeline is set up correctly"

   Typical plan sections to check: Verification, Testing, Success Criteria, Completion Criteria

6. **Non-Goals**: Extract explicitly mentioned scope boundaries or future work items

   Scope guidance:
   - Extract specific exclusions from the plan
   - Look for "out of scope", "future work", "phase 2" mentions
   - Identify related work that's intentionally deferred
   - Be specific about what's excluded

   Example (good): "Multi-region deployment - deferred to Phase 2"
   Example (good): "Automated performance testing - out of scope for MVP pipeline"

   Example (bad): "Other improvements"
   Example (bad): "Advanced features"

   Typical plan sections to check: Out of Scope, Future Work, Non-Goals, Phase 2
{context_section}
Common mistakes to avoid:

❌ **Extracting HOW instead of WHAT**: "Implement Redis caching" (HOW) vs "Reduce API response time to <200ms" (WHAT)
❌ **Listing plan steps as requirements**: Steps are implementation; extract the outcome those steps achieve
❌ **Technical architecture as problem**: "Need microservices" is HOW; "Need independent service scaling" is WHAT
❌ **Vague synthesis**: Plans have specifics—preserve them (metrics, timelines, constraints)
❌ **Missing priorities**: Plans often indicate critical vs optional—use this to assign [MUST HAVE]/[SHOULD HAVE]
❌ **Inventing content**: Extract only what's in the plan or clearly implied by context

7. **Risks**: Extract key risks or failure modes noted in the plan

   Example (good): "Risk of deployment rollback causing downtime if health checks fail"
   Example (good): "Risk of manual approvals slowing releases"

Return your response using YAML frontmatter followed by optional markdown body:

---
problem_statement: "Clear description of the problem..."
assumptions:
  - "First assumption"
  - "Second assumption"
requirements:
  - "[MUST HAVE] First requirement"
  - "[SHOULD HAVE] Second requirement"
constraints:
  - "First constraint"
  - "Second constraint"
acceptance_criteria:
  - "First criterion"
  - "Second criterion"
non_goals:
  - "First non-goal"
  - "Second non-goal"
risks:
  - "First risk"
  - "Second risk"
{yaml_section}---

# Additional Context (Optional)

You may include additional explanatory notes, diagrams, or clarifications here in markdown format if needed.

Note on extraction from plans:
- Plans describe HOW (implementation steps); you extract WHAT (desired outcome)
- Deliverables = WHAT will exist after the plan; Steps = HOW to create deliverables
- If plan says "Step 1: Add authentication middleware", extract \
"User authentication required before API access"
- Assign priorities based on plan emphasis (MVP, critical, stretch goals, etc.)
- Preserve metrics, timelines, and constraints mentioned in the plan
- If plan is vague about outcomes, infer from the steps but mark as synthesis"""


__all__ = ["build_intent_generation_prompt"]
