from app.services.model2_similarity import run_similarity

# Simulated Model 1 output (student answer)
student_answer = (
    "The operating system manages hardware resources "
    "and provides services to applications. "
    "It acts as an interface between the user and the hardware."
)

# Simulated answer key (correct answer)
answer_key = (
    "An operating system manages hardware and software resources. "
    "It provides services to applications and acts as an interface "
    "between the user and the computer hardware."
)

result = run_similarity(student_answer, answer_key)

print("=== Model 2 Output ===")
print(f"Keywords found : {result['keywords']}")
print(f"Similarity Score: {result['similarity_score']}%")
print(f"Missing Keywords: {result['missing_keywords']}")
