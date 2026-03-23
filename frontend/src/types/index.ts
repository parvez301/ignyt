export interface User {
  id: string;
  username: string;
  email: string;
  display_name: string;
  avatar: string;
  theme: string;
  total_xp: number;
  level: number;
}

export interface GeneratedQuestionItem {
  generated_question_id: string;
  type: string;
  question_html: string;
  options?: string[] | Record<string, unknown>;
}
