export interface UserOut {
  id: string;
  email: string;
  name: string;
  interface_mode: string;
  target_track: string | null;
}

export interface SkillOut {
  id: string;
  key: string;
  name: string;
  chapter: string;
  level: number;
  description: string;
}

export interface SkillLessonOut extends SkillOut {
  concept_markdown: string;
  mnemonic: string;
  comic_script: ComicPanelOut[];
}

export interface UserSkillOut {
  skill_key: string;
  skill_name: string;
  chapter: string;
  mastery: number;
  confidence: number;
  attempts: number;
  correct_attempts: number;
  pattern_recognition_accuracy: number | null;
  transfer_accuracy: number | null;
}

export interface TrackTierStatusOut {
  track: string;
  current_tier: string;
  next_tier: string | null;
  detail: string;
  active_assessment_id: string | null;
}

export interface TrackAssessmentItemOut {
  kind: "problem" | "quiz" | "case";
  slug: string;
  title: string;
  options: string[] | null;
}

export interface TrackAssessmentStartOut {
  ok: boolean;
  reason: string | null;
  assessment_id: string | null;
  target_tier: string | null;
  items: TrackAssessmentItemOut[];
}

export interface QuizAnswerResponse {
  correct: boolean;
  correct_index: number;
  explanation: string;
}

export interface TrackAssessmentCheckItem {
  kind: "problem" | "quiz" | "case";
  slug: string;
  title: string;
  score: number;
  passed: boolean;
  reason: string;
  options: string[] | null;
}

export interface TrackAssessmentCheckOut {
  status: string;
  target_tier: string;
  aggregate_score: number | null;
  checks: TrackAssessmentCheckItem[];
}

export interface SkillReadinessOut {
  skill_key: string;
  ready: boolean;
  unmet_prerequisites: string[];
}

export interface ConceptMapNodeOut {
  key: string;
  name: string;
  chapter: string;
}

export interface ConceptMapOut {
  current: ConceptMapNodeOut;
  prerequisites: ConceptMapNodeOut[];
  unlocks: ConceptMapNodeOut[];
}

export interface LessonConceptMapNodeOut {
  slug: string;
  title: string;
  category: string;
  level: number;
}

export interface LessonConceptMapOut {
  current: LessonConceptMapNodeOut;
  previous: LessonConceptMapNodeOut | null;
  next: LessonConceptMapNodeOut | null;
}

export interface BlindPracticeOut {
  available: boolean;
  problem_slug: string | null;
  reason: string;
}

export interface ProblemListItem {
  id: string;
  slug: string;
  title: string;
  difficulty: string;
  primary_skill_key: string;
  concept_difficulty: number;
  implementation_difficulty: number;
  reasoning_difficulty: number;
  pattern_difficulty: number;
  solved: boolean;
  attempted: boolean;
}

export interface TransferChallengeOut {
  available: boolean;
  problem_slug: string | null;
  problem_title: string | null;
  reason: string;
}

export interface VisibleTestCase {
  args: unknown[];
  expected_output: unknown;
  explanation: string;
}

export interface ProblemDetail {
  id: string;
  slug: string;
  title: string;
  statement_markdown: string;
  difficulty: string;
  constraints_markdown: string;
  examples: { input: string; output: string; explanation: string }[];
  function_name: string;
  param_names: string[];
  starter_code: string;
  language: string;
  supported_languages: string[];
  time_limit_ms: number;
  expected_complexity: string;
  primary_skill_key: string;
  visible_test_cases: VisibleTestCase[];
}

export interface TestResultOut {
  index: number;
  passed: boolean;
  is_hidden: boolean;
  input: unknown[] | null;
  expected: unknown;
  actual: unknown;
  error: string | null;
}

export interface Diagnosis {
  primary_issue: string;
  confidence: number;
  evidence: string[];
  recommendation: string;
}

export interface RunResponse {
  status: string;
  passed_count: number;
  total_count: number;
  runtime_ms: number;
  test_results: TestResultOut[];
}

export interface SubmitResponse {
  submission_id: string;
  status: string;
  passed_count: number;
  total_count: number;
  runtime_ms: number;
  test_results: TestResultOut[];
  diagnosis: Diagnosis | null;
  updated_mastery: number | null;
  repeat_solve_note: string | null;
  optimization_nudge: string | null;
  language: string;
  runtime_percentile: number | null;
}

export interface ComplexitySampleOut {
  size: number;
  status: string;
  runtime_ms: number | null;
}

export interface ComplexityCheckResponse {
  supported: boolean;
  reason: string | null;
  samples: ComplexitySampleOut[];
  estimated_exponent: number | null;
  estimated_label: string | null;
  expected_complexity: string;
  likely_matches_expected: boolean | null;
  explanation: string;
}

export interface TraceStepOut {
  line: number;
  depth: number;
  locals: Record<string, unknown>;
}

export interface TraceResponse {
  supported: boolean;
  reason: string | null;
  status: string | null;
  error_message: string | null;
  result: unknown;
  steps: TraceStepOut[];
  truncated: boolean;
  source_lines: string[];
}

export interface SubmissionHistoryItem {
  id: string;
  status: string;
  language: string;
  passed_count: number;
  total_count: number;
  runtime_ms: number;
  created_at: string;
  code: string;
}

export interface ExplainResponse {
  explanation: string;
  grounded_in: string[];
}

export interface AskResponse {
  answer: string;
}

export interface PlanQualityCoachOut {
  plan_quality_tier: string;
  coaching_tip: string;
  confidence: number;
}

export interface ReasoningSubmitResponse {
  is_correct_pattern: boolean;
  correct_pattern: string;
  reasoning_quality_score: number;
  evidence_matched: string[];
  missing_evidence: string[];
  declared_pattern_evidence: string[];
  feedback: string;
  plan_quality_coach: PlanQualityCoachOut | null;
}

export interface RecommendationOut {
  id: string;
  activity_type: string;
  skill_key: string | null;
  problem_slug: string | null;
  reason_what: string;
  reason_why: string;
  expected_outcome: string;
}

export interface DueReviewOut {
  review_id: string;
  skill_key: string;
  skill_name: string;
  due_at: string;
  interval_days: number;
  repetitions: number;
}

export interface DimensionScore {
  label: string;
  score: number | null;
  evidence_count: number;
}

export interface DashboardOut {
  interview_readiness: Record<string, DimensionScore>;
  overall_readiness: number | null;
  weakest_skills: { skill_key: string; mastery: number }[];
  retention_due_count: number;
  total_submissions: number;
  total_solved: number;
  current_streak_days: number;
  active_days_last_30: number;
}

export interface HabitProfileOut {
  available: boolean;
  reason: string | null;
  habit: string | null;
  coaching_tip: string | null;
  confidence: number | null;
  features: {
    reasoning_usage_rate: number;
    avg_hints_per_problem: number;
    avg_submissions_per_problem: number;
    solve_rate: number;
    n_problems_attempted: number;
    n_submissions: number;
  } | null;
}

export interface SystemDesignCaseOut {
  id: string;
  slug: string;
  title: string;
  difficulty: string;
  base_slug: string | null;
  scale_tier: string | null;
  scale_description: string | null;
  description_markdown: string;
  functional_requirements: string[];
  non_functional_requirements: string[];
  estimation_prompt: string;
  editorial_markdown: string;
}

export interface SystemDesignLessonOut {
  id: string;
  slug: string;
  title: string;
  level: number;
  category: string;
  content_markdown: string;
  dsa_connection: string;
  comic_script: ComicPanelOut[];
}

export interface ScopeCoachOut {
  scope_verdict: string;
  coaching_tip: string;
  confidence: number;
}

export interface SystemDesignAttemptResponse {
  score: number;
  missing_components: string[];
  unjustified_components: string[];
  estimation_feedback: Record<string, { status: string; submitted?: number; expected_order_of_magnitude: number; unit: string }>;
  why_questions: string[];
  scope_coach: ScopeCoachOut | null;
}

export interface LLDCaseOut {
  id: string;
  slug: string;
  title: string;
  difficulty: string;
  description_markdown: string;
  functional_requirements: string[];
  non_functional_requirements: string[];
  abstraction_hint: string;
  editorial_markdown: string;
}

export interface LLDClassIn {
  name: string;
  fields: string[];
  methods: string[];
  extends: string | null;
  implements: string[];
}

export interface LLDAttemptResponse {
  score: number;
  missing_classes: string[];
  extra_classes: string[];
  uses_abstraction: boolean;
  god_classes: string[];
  why_questions: string[];
}

export interface InterviewMessageOut {
  role: string;
  stage: string;
  content: string;
}

export interface StartInterviewResponse {
  session_id: string;
  stage: string;
  messages: InterviewMessageOut[];
}

export interface AnswerResponse {
  stage: string;
  finished: boolean;
  messages: InterviewMessageOut[];
  commentary: string | null;
}

export interface ContestProblemOut {
  slug: string;
  title: string;
  difficulty: string;
}

export interface ContestOut {
  id: string;
  title: string;
  start_at: string;
  end_at: string;
  status: "upcoming" | "live" | "ended";
  problem_count: number;
}

export interface ContestDetailOut extends ContestOut {
  problems: ContestProblemOut[];
}

export interface LeaderboardEntryOut {
  rank: number;
  user_name: string;
  total_score: number;
  problems_solved: number;
}

export interface ComicPanelOut {
  speaker: string;
  text: string;
}

export interface NetworkLessonOut {
  id: string;
  slug: string;
  title: string;
  level: number;
  category: string;
  content_markdown: string;
  practical_connection: string;
  comic_script: ComicPanelOut[];
}

export interface NetworkQuizQuestionOut {
  id: string;
  question: string;
  options: string[];
}

export interface NetworkQuizAnswerOut {
  correct: boolean;
  correct_index: number;
  explanation: string;
}

export interface InterviewReport {
  stages_completed: number;
  total_stages: number;
  transcript: InterviewMessageOut[];
  coverage_score: number;
  summary: string;
}

export interface MockLoopStartResponse {
  loop_id: string;
  stage: string;
  dsa_problem_slug: string;
  dsa_problem_title: string;
  sd_case_slug: string;
  sd_case_title: string;
  behavioral_question: string;
}

export interface MockLoopStateOut {
  loop_id: string;
  stage: string;
  dsa_problem_slug: string;
  dsa_submitted: boolean;
  dsa_passed: boolean | null;
  sd_case_slug: string;
  sd_submitted: boolean;
  sd_score: number | null;
  behavioral_question: string;
  behavioral_submitted: boolean;
}

export interface MockLoopReportOut {
  dsa_problem_title: string;
  dsa_passed: boolean | null;
  dsa_passed_count: number | null;
  dsa_total_count: number | null;
  sd_case_title: string;
  sd_score: number | null;
  sd_missing_components: string[];
  sd_unjustified_components: string[];
  behavioral_question: string;
  behavioral_tier: string | null;
  behavioral_coaching_tip: string | null;
  behavioral_star_score: number | null;
  overall_summary: string;
}

export interface AskLessonResponse {
  answer: string;
}

export interface ExplainBackResponse {
  quality_tier: string;
  coaching_tip: string;
  confidence: number;
  matched_terms: string[];
}

export interface ConceptBridgeItem {
  domain: "dsa" | "system_design" | "networks";
  key: string;
  title: string;
  similarity: number;
}

export interface ConceptBridgeResponse {
  bridges: ConceptBridgeItem[];
}

export interface CheatSheetItem {
  key: string;
  title: string;
  mnemonic: string | null;
  key_takeaway: string;
}

export interface CheatSheetGroup {
  group: string;
  items: CheatSheetItem[];
}

export interface ConceptBridgePairOut {
  a_domain: "dsa" | "system_design" | "networks";
  a_key: string;
  a_title: string;
  b_domain: "dsa" | "system_design" | "networks";
  b_key: string;
  b_title: string;
  similarity: number;
}
