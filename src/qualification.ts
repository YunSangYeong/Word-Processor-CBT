// Official site access was denied by the environment proxy; these are disclosed learning assumptions.
export const PROFILE = {
  name: "워드프로세서", bankId: "main", questionCount: 60, durationMinutes: 60,
  choiceCount: 4, questionsPerSubject: 20, passScore: 60, subjectCutoff: 40,
  subjects: ["워드프로세싱 용어 및 기능", "PC 운영체제", "PC 기본상식"] as const,
  rulesVerificationStatus: "pending", targetReviewedCount: 1000,
  officialSource: "https://license.korcham.net/",
} as const;
