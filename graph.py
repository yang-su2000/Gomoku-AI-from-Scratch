import matplotlib.pyplot as plt

# constant
MAX_ITERATIONS = 50
AI_count = 3
Human_score = 1
AI_0_to_human_success_rate = 0.75
Not_applicable_score = -1

# setup
score_list = []
for i in range(AI_count):
    score_list.append([0] * MAX_ITERATIONS)
    score_list[i][0] = 1 / AI_count

# initialization
# AIx_score = [AIx vs. Human avg, AIx vs. AI0 avg, AIx vs. AI1 avg, ... , AIx vs AIn avg]
# AIx vs. AIy avg = AIx black win rate to AIy + AIx white win rate to AIy
# AIx emits to AIy = 1 / AIx vs. AIy avg
AI0_score = [Not_applicable_score, 1 / (45 / 69 + 57 / 86), 1 / (32 / 44 + 29 / 45)]
AI1_score = [1 / (86 / 57 + 69 / 45), Not_applicable_score, 1 / (43 / 46 + 33 / 53)]
AI2_score = [1 / (45 / 29 + 44 / 32), 1 / (53 / 33 + 46 / 43), Not_applicable_score]
AI_score = [AI0_score, AI1_score, AI2_score]
# print(AI_score)

# normalize
for i in range(AI_count):
    sum_score = 0
    for j in range(AI_count):
        if AI_score[i][j] != Not_applicable_score:
            sum_score += AI_score[i][j]
    for j in range(AI_count):
        if AI_score[i][j] != Not_applicable_score:
            AI_score[i][j] /= sum_score
# print(AI_score)
# markov process
for i in range(MAX_ITERATIONS - 1):
    for receiver in range(AI_count):
        for emitter in range(AI_count):
            if AI_score[emitter][receiver] != Not_applicable_score:
                score_list[receiver][i + 1] += score_list[emitter][i] * AI_score[emitter][receiver]
                #print("At " + str(i + 1) + " iteration, AI " + str(receiver) + " get score of " + str(score_list[emitter][i]) + " * " + str(AI_score[emitter][receiver]) + " from AI " + str(emitter))

# print(score_list[0])
# print(score_list[1])
# print(score_list[2])
multiplier = AI_0_to_human_success_rate * 2 * Human_score / score_list[0][MAX_ITERATIONS - 1]
for i in range(AI_count):
    for j in range(MAX_ITERATIONS):
        score_list[i][j] *= multiplier
human_list = [Human_score] * MAX_ITERATIONS
plt.plot(human_list, label="Human")
for i in range(AI_count):
    plt.plot(score_list[i], label="AI " + str(i))
plt.legend(loc="right")
plt.title("Intelligence Level vs. Iterations")
plt.show()