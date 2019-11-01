import numpy as np
from sklearn import preprocessing as pr
import matplotlib.pylab as plt

scores_rand_against = [55.4,3.6,2.8,3.1,3.7]
scores_mm3_against = [96.8,70.2,35.4,68.6,29.8]
scores_mm5_against = [97.4,92.6,89.0,90.2,87.8]
scores_mmab3_against = [97.2,72.4,31.2,69.8,30.0]
scores_mmab5_against = [99.0,91.2,88.4,93.2,89.4]

score_matrix = [scores_rand_against, scores_mm3_against, scores_mm5_against, scores_mmab3_against, scores_mmab5_against]
score_matrix = np.asarray(score_matrix)
print(score_matrix.shape)

fig1, ax1 = plt.subplots()
min_val, max_val = 0,100
im = ax1.matshow(score_matrix, cmap=plt.cm.Reds)
ax1.set_xlabel('Second Player')
ax1.set_xticklabels(('first', 'rand','mm3','mm5','mmab3','mmab5'))
ax1.set_ylabel('First Player')
ax1.set_yticklabels(('second',  'rand','mm3','mm5','mmab3','mmab5'))
ax1.set_title('Winning rates of games between different algorithms')
for i in range(0, len(scores_mm3_against)):
    for j in range(0, len(scores_mm3_against)):
        Str = str(score_matrix[j][i])
        ax1.text(i,j, Str, va='center', ha='center')
fig1.colorbar(im)
fig1.tight_layout()
plt.show()

# comparison of pruning / no pruning Runtime
fig, ax = plt.subplots()
index = np.arange(5)
bar_width = 0.3
opacity = 0.4
pruning_time = (0.1106, 0.1391, 0.2898, 0.7925, 2.9910)

nopruning_time = (0.1087, 0.1315, 0.1764, 0.2685, 0.8905)

fig2, ax2 = plt.subplots()

rects1 = ax2.bar(index, pruning_time, bar_width, alpha=opacity, color='b', label="minimax")
rects2 = ax2.bar(index + bar_width, nopruning_time, bar_width, alpha=opacity, color='r', label="alphabeta")

ax2.set_xlabel('Max depth')
ax2.set_ylabel('Runtime [s]')
ax2.set_title('Runtime by max depth and pruning')
ax2.set_xticks(index + bar_width / 2)
ax2.set_xticklabels(('3','4','5','6','7'))
ax2.legend()
fig2.tight_layout()
plt.show()
