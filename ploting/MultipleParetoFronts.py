import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def extract_points(file_content):
    """
    Extracts points (x, y) from the given file content.
    
    :param file_content: File content as a string.
    :return: List of points (x, y) as tuples.
    """
    points = []
    for line in file_content.strip().split("\n"):
        # Removes parentheses and splits elements
        elements = eval(line.strip())
        x = elements[2]  # Third element
        y = elements[3]  # Fourth element
        points.append((x, y))
    return points

def visualize_convex_hull(pareto_fronts, labels):
    plt.figure(figsize=(10, 6))
    ax = plt.gca()  # Get axes for later manipulation

    for idx, pareto_front in enumerate(pareto_fronts):
        x = np.array([point[1] for point in pareto_front])  # Toxicity
        y = np.array([point[0] for point in pareto_front])  # AMP probability

        sorted_indices = np.argsort(x)
        sorted_x = x[sorted_indices]
        sorted_y = y[sorted_indices]

        x_hull = np.concatenate(([0], sorted_x))
        y_hull = np.concatenate(([1], sorted_y))

        label_text = f"{['First', 'Second', 'Third', 'Fourth', 'Fifth'][idx]} algorithm execution"
        ax.plot(x_hull, y_hull, marker='o', linestyle='', label=label_text, markersize=14)

    # First legend – automatic, related to Pareto fronts
    legend1 = ax.legend(loc='lower left', fontsize=25, title_fontsize=25)
    ax.add_artist(legend1)  # Add manually so another legend can be added later

    # Create empty black and gray circles for the legend
    empty_black_circle = Line2D([0], [0], marker='o', markerfacecolor='none',
                                markeredgewidth=2, markersize=18, color='black',
                                label='High AMP potential, increased toxicity', linestyle='none')
    empty_gray_circle = Line2D([0], [0], marker='o', markerfacecolor='none',
                               markeredgewidth=2, markersize=18, color='gray',
                               label='Lower AMP activity, reduced toxicity', linestyle='none')

    # Add empty circles to legend
    ax.legend(handles=[empty_black_circle, empty_gray_circle],
              loc='lower right', title='Marked area',
              fontsize=25, title_fontsize=25)

    ax.set_title("Comparison of Pareto fronts across algorithm executions", fontsize=30)
    ax.set_xlabel("Toxicity fitness value", fontsize=30)
    ax.set_ylabel("AMP Probability fitness value", fontsize=30)

    # Increase font size of axis ticks
    ax.tick_params(axis='both', which='major', labelsize=24)

    # Limit y-axis from 0.55 to 1 for better readability
    ax.set_ylim(0.55, 1)

    # Automatically set x-axis as before
    ax.set_xlim(0, max([np.array([point[1] for point in pf]).max() for pf in pareto_fronts]) * 1.1)

    ax.grid(True)
    ax.set_aspect('auto')
    plt.show()


file_content1="""
(['T', 'K', 'P', 'F', 'E', 'R', 'M', 'W', 'G', 'K', 'I', 'Y', 'H', 'K', 'E', 'L', 'V', 'W'], 'TKPFERMWGKIYHKELVW', 0.84, 2.77)
(['T', 'H', 'V', 'K', 'Q', 'P', 'L', 'W', 'G', 'K', 'S', 'H', 'H', 'K', 'E', 'W', 'F'], 'THVKQPLWGKSHHKEWF', 0.9867245196432676, 1.54)
(['D', 'W', 'V', 'R', 'R', 'P', 'L', 'Q', 'P', 'Q', 'K', 'W', 'H', 'K', 'E', 'W', 'P', 'W'], 'DWVRRPLQPQKWHKEWPW', 0.9955495850275018, 0.95)
(['T', 'K', 'P', 'F', 'Q', 'P', 'L', 'Q', 'P', 'Q', 'K', 'W', 'H', 'K', 'E', 'W', 'P', 'W'], 'TKPFQPLQPQKWHKEWPW', 0.9812661672605639, 1.72)
(['T', 'K', 'P', 'F', 'E', 'R', 'M', 'Q', 'E', 'V', 'A', 'Y', 'H', 'K', 'E', 'W', 'F'], 'TKPFERMQEVAYHKEWF', 0.9068271370427544, 2.54)
(['N', 'W', 'H', 'E', 'F', 'I', 'Q', 'R', 'I', 'Q', 'I', 'Y', 'H', 'K', 'E', 'L', 'G', 'L', 'C'], 'NWHEFIQRIQIYHKELGLC', 0.9540349131338318, 2.07)
(['T', 'K', 'P', 'F', 'E', 'R', 'L', 'P', 'E', 'Q', 'I', 'Y', 'W', 'R', 'Y', 'A', 'F'], 'TKPFERLPEQIYWRYAF', 0.9506247241013419, 2.17)
(['N', 'W', 'H', 'E', 'F', 'I', 'Q', 'R', 'I', 'V', 'A', 'Y', 'H', 'K', 'E', 'W', 'F'], 'NWHEFIQRIVAYHKEWF', 0.9610402174842412, 1.96)
(['T', 'H', 'V', 'K', 'Q', 'P', 'L', 'W', 'G', 'K', 'S', 'H', 'H', 'K', 'E', 'W', 'V', 'W'], 'THVKQPLWGKSHHKEWVW', 0.9853670494407594, 1.65)
(['D', 'W', 'V', 'K', 'Q', 'P', 'L', 'Q', 'P', 'Q', 'K', 'W', 'H', 'K', 'E', 'W', 'P', 'W'], 'DWVKQPLQPQKWHKEWPW', 0.9914966688180631, 1.12)
(['T', 'K', 'P', 'F', 'E', 'R', 'M', 'W', 'G', 'K', 'I', 'Y', 'H', 'K', 'T', 'S', 'G', 'L', 'C'], 'TKPFERMWGKIYHKTSGLC', 0.9258590415719372, 2.46)
(['N', 'W', 'H', 'E', 'F', 'I', 'Q', 'R', 'I', 'Q', 'S', 'Y', 'W', 'R', 'T', 'L', 'V', 'W'], 'NWHEFIQRIQSYWRTLVW', 0.96713915630975, 1.78)
(['T', 'K', 'P', 'F', 'E', 'R', 'M', 'W', 'G', 'K', 'I', 'Y', 'W', 'R', 'T', 'L', 'G', 'L', 'C'], 'TKPFERMWGKIYWRTLGLC', 0.938705803680136, 2.3)
(['T', 'K', 'P', 'F', 'E', 'R', 'M', 'W', 'G', 'K', 'I', 'Y', 'W', 'R', 'T', 'L', 'V', 'W'], 'TKPFERMWGKIYWRTLVW', 0.9098963486326275, 2.51)
(['T', 'K', 'P', 'F', 'E', 'R', 'M', 'W', 'G', 'K', 'I', 'Y', 'W', 'R', 'T', 'L', 'V', 'Y'], 'TKPFERMWGKIYWRTLVY', 0.9155684572606141, 2.5)
(['T', 'H', 'V', 'K', 'Q', 'P', 'L', 'W', 'G', 'K', 'I', 'Y', 'W', 'R', 'T', 'L', 'V', 'Y'], 'THVKQPLWGKIYWRTLVY', 0.9658104768256116, 1.8)
(['D', 'W', 'V', 'R', 'R', 'A', 'M', 'W', 'G', 'K', 'I', 'Y', 'H', 'K', 'E', 'W', 'F'], 'DWVRRAMWGKIYHKEWF', 0.9715260630153232, 1.75)
(['T', 'W', 'H', 'F', 'E', 'R', 'M', 'W', 'G', 'K', 'I', 'Y', 'N', 'K', 'Y', 'W', 'P', 'C'], 'TWHFERMWGKIYNKYWPC', 0.9668676768863342, 1.78)
(['T', 'K', 'P', 'F', 'E', 'R', 'L', 'W', 'G', 'K', 'I', 'Y', 'W', 'R', 'T', 'L', 'V', 'Y'], 'TKPFERLWGKIYWRTLVY', 0.9321621643590955, 2.32)
(['T', 'K', 'P', 'F', 'E', 'R', 'M', 'Q', 'P', 'Q', 'I', 'Y', 'H', 'K', 'E', 'L', 'G', 'L', 'C'], 'TKPFERMQPQIYHKELGLC', 0.8595616066873093, 2.68)
(['N', 'W', 'H', 'W', 'E', 'R', 'L', 'P', 'E', 'D', 'I', 'Y', 'H', 'K', 'E', 'W', 'F'], 'NWHWERLPEDIYHKEWF', 0.9514068694198907, 2.09)
(['T', 'K', 'P', 'F', 'E', 'R', 'M', 'R', 'I', 'Q', 'I', 'Y', 'H', 'E', 'Y', 'A', 'F'], 'TKPFERMRIQIYHEYAF', 0.8919130025019494, 2.67)
(['T', 'K', 'P', 'F', 'E', 'R', 'M', 'Q', 'I', 'K', 'I', 'Y', 'H', 'K', 'E', 'L', 'V', 'W'], 'TKPFERMQIKIYHKELVW', 0.8295845119939613, 2.88)
(['T', 'K', 'P', 'F', 'Q', 'P', 'L', 'Q', 'P', 'Q', 'A', 'Y', 'H', 'K', 'E', 'L', 'V', 'C'], 'TKPFQPLQPQAYHKELVC', 0.9549442128502618, 2.02)
"""

file_content2="""
(['V', 'W', 'E', 'R', 'T', 'L', 'K', 'E', 'L', 'P', 'H', 'H', 'K', 'Y', 'L', 'R'], 'VWERTLKELPHHKYLR', 0.9416928449003052, 2.21)
(['H', 'W', 'E', 'R', 'L', 'A', 'F', 'A', 'G', 'W', 'H', 'H', 'K', 'V', 'S', 'S', 'I', 'H', 'H'], 'HWERLAFAGWHHKVSSIHH', 0.9814637405724603, 1.7)
(['H', 'I', 'E', 'R', 'T', 'L', 'K', 'E', 'L', 'L', 'M', 'A', 'I', 'Y', 'L', 'S', 'H', 'H'], 'HIERTLKELLMAIYLSHH', 0.8932987708072149, 2.37)
(['H', 'I', 'Y', 'L', 'A', 'L', 'K', 'E', 'W', 'G', 'L', 'T', 'K', 'Y', 'L', 'N', 'I', 'H'], 'HIYLALKEWGLTKYLNIH', 0.9066630595116887, 2.25)
(['H', 'I', 'Y', 'L', 'A', 'L', 'K', 'E', 'L', 'P', 'H', 'A', 'I', 'Y', 'L', 'S', 'I', 'H'], 'HIYLALKELPHAIYLSIH', 0.9086330648625435, 2.24)
(['H', 'K', 'E', 'R', 'T', 'L', 'I', 'E', 'L', 'P', 'L', 'H', 'K', 'Y', 'L', 'N', 'I', 'T'], 'HKERTLIELPLHKYLNIT', 0.8697644557537515, 2.53)
(['H', 'K', 'E', 'R', 'T', 'L', 'I', 'E', 'L', 'P', 'L', 'A', 'I', 'Y', 'L', 'S', 'H', 'H'], 'HKERTLIELPLAIYLSHH', 0.8260275507945912, 2.57)
(['H', 'K', 'H', 'F', 'P', 'A', 'F', 'A', 'G', 'F', 'M', 'T', 'K', 'V', 'L', 'N', 'I', 'H'], 'HKHFPAFAGFMTKVLNIH', 0.9717203008621867, 1.92)
(['V', 'W', 'E', 'R', 'L', 'L', 'K', 'A', 'G', 'F', 'M', 'T', 'K', 'Y', 'L', 'S', 'H'], 'VWERLLKAGFMTKYLSH', 0.947512471522067, 2.07)
(['V', 'W', 'E', 'R', 'T', 'L', 'K', 'A', 'G', 'F', 'M', 'T', 'K', 'V', 'L', 'S', 'H', 'H'], 'VWERTLKAGFMTKVLSHH', 0.9495821383731643, 2.04)
(['H', 'K', 'H', 'F', 'P', 'A', 'F', 'A', 'G', 'F', 'M', 'T', 'K', 'V', 'S', 'S', 'I', 'H', 'H'], 'HKHFPAFAGFMTKVSSIHH', 0.9844638321234291, 1.58)
(['H', 'K', 'E', 'R', 'T', 'L', 'I', 'E', 'W', 'G', 'L', 'T', 'K', 'Y', 'L', 'R'], 'HKERTLIEWGLTKYLR', 0.8886648791328472, 2.44)
(['H', 'H', 'K', 'F', 'P', 'A', 'F', 'A', 'G', 'F', 'M', 'T', 'K', 'V', 'L', 'N', 'I', 'H'], 'HHKFPAFAGFMTKVLNIH', 0.9719611452437693, 1.77)
(['H', 'H', 'K', 'F', 'P', 'A', 'F', 'A', 'G', 'F', 'M', 'T', 'K', 'V', 'S', 'S', 'I', 'H', 'H'], 'HHKFPAFAGFMTKVSSIHH', 0.9845761595788373, 1.39)
(['H', 'K', 'E', 'R', 'T', 'L', 'I', 'K', 'T', 'W', 'H', 'H', 'I', 'D', 'L', 'N', 'I', 'T'], 'HKERTLIKTWHHIDLNIT', 0.9405493528475432, 2.24)
(['H', 'T', 'L', 'H', 'R', 'V', 'K', 'K', 'G', 'W', 'H', 'H', 'K', 'V', 'S', 'S', 'I', 'H', 'H'], 'HTLHRVKKGWHHKVSSIHH', 0.9862135076255639, 1.11)
(['T', 'W', 'L', 'H', 'R', 'V', 'K', 'K', 'W', 'G', 'P', 'H', 'A', 'V', 'S', 'S', 'I', 'H', 'H'], 'TWLHRVKKWGPHAVSSIHH', 0.9978996371489537, 0.91)
(['H', 'I', 'E', 'R', 'T', 'L', 'K', 'E', 'L', 'L', 'M', 'A', 'I', 'Y', 'L', 'R'], 'HIERTLKELLMAIYLR', 0.8739840263990992, 2.45)
"""

file_content3="""
(['Y', 'W', 'H', 'Q', 'L', 'T', 'A', 'I', 'L', 'L', 'K', 'M', 'G', 'V', 'A', 'M', 'L', 'C'], 'YWHQLTAILLKMGVAMLC', 0.9478667314099519, 1.83)
(['Q', 'D', 'F', 'Q', 'R', 'Y', 'P', 'R', 'G', 'A', 'P', 'K', 'P', 'V', 'F', 'K', 'P', 'V'], 'QDFQRYPRGAPKPVFKPV', 0.986715510694341, 1.34)
(['N', 'Y', 'R', 'R', 'L', 'K', 'I', 'H', 'G', 'F', 'R', 'W', 'G', 'V', 'T', 'K', 'P', 'V', 'T'], 'NYRRLKIHGFRWGVTKPVT', 0.8099999999999999, 2.36)
(['N', 'W', 'H', 'A', 'T', 'K', 'I', 'W', 'V', 'Q', 'Q', 'W', 'G', 'V', 'T', 'K', 'P', 'R', 'I'], 'NWHATKIWVQQWGVTKPRI', 0.9126580774784582, 2.17)
(['N', 'W', 'H', 'A', 'T', 'K', 'I', 'H', 'M', 'D', 'L', 'V', 'V', 'R', 'I', 'M', 'L', 'C'], 'NWHATKIHMDLVVRIMLC', 0.9593990192887883, 1.74)
(['Y', 'W', 'H', 'Q', 'L', 'T', 'A', 'I', 'G', 'F', 'R', 'W', 'G', 'V', 'T', 'K', 'P', 'V', 'T'], 'YWHQLTAIGFRWGVTKPVT', 0.7891557506688627, 2.43)
(['Q', 'D', 'Y', 'I', 'K', 'Q', 'I', 'W', 'C', 'K', 'I', 'M', 'H', 'P', 'I', 'N', 'G', 'I'], 'QDYIKQIWCKIMHPINGI', 0.9899999739641103, -0.16)
(['N', 'Y', 'F', 'R', 'R', 'Y', 'P', 'R', 'F', 'F', 'R', 'S', 'F', 'G', 'V', 'A', 'M', 'L', 'R', 'I'], 'NYFRRYPRFFRSFGVAMLRI', 0.9787296850581688, 1.62)
(['N', 'W', 'H', 'A', 'F', 'Y', 'H', 'E', 'V', 'H', 'K', 'M', 'G', 'V', 'A', 'M', 'L', 'C'], 'NWHAFYHEVHKMGVAMLC', 0.9498234644742736, 1.75)
(['N', 'Y', 'F', 'R', 'R', 'Y', 'P', 'R', 'F', 'F', 'R', 'M', 'H', 'P', 'I', 'N', 'G', 'I'], 'NYFRRYPRFFRMHPINGI', 0.989575076795711, 0.8)
(['N', 'W', 'H', 'A', 'T', 'K', 'I', 'H', 'M', 'D', 'L', 'V', 'G', 'V', 'A', 'M', 'L', 'C'], 'NWHATKIHMDLVGVAMLC', 0.9281218635128639, 1.9)
(['N', 'W', 'H', 'A', 'T', 'K', 'I', 'W', 'V', 'Q', 'Q', 'W', 'G', 'V', 'T', 'K', 'G', 'I'], 'NWHATKIWVQQWGVTKGI', 0.9490786108748336, 1.77)
(['N', 'W', 'H', 'A', 'T', 'K', 'I', 'W', 'V', 'Q', 'Q', 'W', 'G', 'V', 'T', 'K', 'P', 'R'], 'NWHATKIWVQQWGVTKPR', 0.918579075078887, 2.0)
(['N', 'Y', 'F', 'R', 'R', 'Y', 'P', 'R', 'F', 'F', 'R', 'S', 'G', 'V', 'A', 'M', 'L', 'L', 'R', 'I'], 'NYFRRYPRFFRSGVAMLLRI', 0.9789276385425122, 1.58)
(['Y', 'Y', 'R', 'S', 'F', 'P', 'I', 'W', 'C', 'K', 'I', 'M', 'H', 'P', 'I', 'N', 'G', 'I'], 'YYRSFPIWCKIMHPINGI', 0.9899877838254203, -0.16)
(['Q', 'D', 'F', 'Q', 'R', 'Y', 'P', 'R', 'G', 'A', 'P', 'K', 'P', 'Y', 'T', 'K', 'P', 'V'], 'QDFQRYPRGAPKPYTKPV', 0.984021131106858, 1.55)
(['K', 'P', 'F', 'R', 'P', 'E', 'P', 'R', 'L', 'L', 'K', 'M', 'G', 'V', 'A', 'M', 'L', 'C'], 'KPFRPEPRLLKMGVAMLC', 0.931880613490983, 1.84)
(['Q', 'D', 'L', 'E', 'R', 'K', 'I', 'H', 'G', 'F', 'R', 'M', 'G', 'V', 'A', 'M', 'L', 'C'], 'QDLERKIHGFRMGVAMLC', 0.9054416778281321, 2.27)
(['Q', 'D', 'Y', 'A', 'T', 'K', 'I', 'H', 'G', 'F', 'R', 'W', 'G', 'V', 'T', 'K', 'P', 'V', 'T'], 'QDYATKIHGFRWGVTKPVT', 0.83630354281713, 2.33)
"""

file_content4="""
(['N', 'W', 'H', 'K', 'E', 'R', 'N', 'R', 'I', 'Y', 'R', 'Q', 'L', 'R', 'R'], 'NWHKERNRIYRQLRR', 0.9047183002819039, 2.36)
(['N', 'W', 'H', 'K', 'E', 'R', 'N', 'R', 'I', 'Y', 'R', 'Q', 'R', 'R'], 'NWHKERNRIYRQRR', 0.9291057091165508, 2.18)
(['H', 'W', 'H', 'K', 'E', 'V', 'R', 'I', 'Y', 'S', 'R', 'Q', 'L', 'R', 'R'], 'HWHKEVRIYSRQLRR', 0.9052789192473161, 2.19)
(['H', 'W', 'W', 'Q', 'N', 'R', 'I', 'H', 'G', 'I', 'W', 'H', 'E', 'R'], 'HWWQNRIHGIWHER', 0.9726148189823123, 1.58)
(['P', 'T', 'V', 'A', 'R', 'R', 'I', 'H', 'K', 'L', 'N', 'M', 'E', 'R'], 'PTVARRIHKLNMER', 0.9024190909948739, 2.43)
(['H', 'W', 'W', 'R', 'L', 'M', 'Q', 'H', 'K', 'L', 'H', 'M', 'P', 'H', 'A', 'Q'], 'HWWRLMQHKLHMPHAQ', 0.9634614291827625, 1.65)
(['H', 'W', 'W', 'R', 'L', 'M', 'Q', 'H', 'K', 'L', 'H', 'M', 'P', 'H', 'A'], 'HWWRLMQHKLHMPHA', 0.9630053090623617, 1.76)
(['H', 'W', 'W', 'R', 'L', 'M', 'Q', 'H', 'K', 'L', 'H', 'M', 'P', 'H'], 'HWWRLMQHKLHMPH', 0.9632908542663216, 1.76)
(['P', 'T', 'V', 'A', 'R', 'R', 'I', 'T', 'C', 'H', 'M', 'E', 'R'], 'PTVARRITCHMER', 0.9593846397065139, 1.77)
(['P', 'T', 'V', 'Q', 'Q', 'L', 'R', 'I', 'T', 'C', 'H', 'M', 'E', 'R'], 'PTVQQLRITCHMER', 0.9321168508615805, 1.85)
(['H', 'W', 'W', 'Q', 'Q', 'G', 'Q', 'W', 'G', 'I', 'W', 'H', 'W', 'P', 'K', 'C'], 'HWWQQGQWGIWHWPKC', 0.986048552894742, 0.6)
(['H', 'W', 'W', 'R', 'L', 'M', 'Q', 'W', 'C', 'H', 'M', 'H', 'W', 'P', 'K'], 'HWWRLMQWCHMHWPK', 0.9880529869192543, 0.05)
(['N', 'W', 'H', 'K', 'E', 'G', 'L', 'H', 'K', 'L', 'Y', 'E', 'H', 'Y'], 'NWHKEGLHKLYEHY', 0.9783847546148743, 1.28)
(['N', 'W', 'H', 'K', 'L', 'G', 'I', 'H', 'G', 'I', 'W', 'H', 'W', 'P', 'K', 'C', 'C', 'C'], 'NWHKLGIHGIWHWPKCCC', 0.9997201133597672, -0.83)
(['N', 'W', 'H', 'K', 'E', 'R', 'I', 'T', 'A', 'L', 'N', 'N', 'F', 'G'], 'NWHKERITALNNFG', 0.8015759700911851, 2.46)
"""

file_content5="""
(['V', 'W', 'M', 'P', 'R', 'F', 'Y', 'R', 'I', 'Y', 'W', 'G', 'H', 'D', 'F', 'Q'], 'VWMPRFYRIYWGHDFQ', 0.7, 3.06)
(['Q', 'R', 'F', 'W', 'N', 'K', 'V', 'T', 'Q', 'Y', 'W', 'G', 'H', 'D', 'F', 'I', 'N', 'E', 'F'], 'QRFWNKVTQYWGHDFINEF', 0.9767426920302075, 1.71)
(['V', 'W', 'M', 'P', 'R', 'F', 'Y', 'R', 'I', 'Y', 'W', 'H', 'K', 'W', 'Q', 'P'], 'VWMPRFYRIYWHKWQP', 0.8147429036091881, 3.04)
(['Q', 'R', 'M', 'P', 'R', 'F', 'Y', 'R', 'I', 'Y', 'W', 'H', 'K', 'W', 'T', 'H'], 'QRMPRFYRIYWHKWTH', 0.9089287043259883, 2.69)
(['N', 'P', 'L', 'E', 'R', 'F', 'A', 'R', 'I', 'Y', 'T', 'K', 'K', 'W', 'Q', 'P'], 'NPLERFARIYTKKWQP', 0.9664444512700684, 2.04)
(['V', 'W', 'M', 'P', 'R', 'F', 'Y', 'R', 'I', 'Y', 'W', 'H', 'K', 'D', 'F', 'I', 'N', 'E', 'F'], 'VWMPRFYRIYWHKDFINEF', 0.8464303891089645, 3.0)
(['Q', 'R', 'F', 'W', 'N', 'F', 'Y', 'N', 'I', 'Y', 'W', 'H', 'K', 'W', 'T', 'C'], 'QRFWNFYNIYWHKWTC', 0.9444215009430792, 2.23)
(['V', 'W', 'M', 'P', 'R', 'F', 'Y', 'N', 'I', 'Y', 'T', 'K', 'W', 'W', 'Q', 'P'], 'VWMPRFYNIYTKWWQP', 0.869086766066629, 2.72)
(['K', 'R', 'M', 'P', 'R', 'F', 'Y', 'R', 'I', 'Y', 'W', 'H', 'K', 'W', 'T', 'H'], 'KRMPRFYRIYWHKWTH', 0.9222534979098311, 2.61)
(['V', 'W', 'M', 'P', 'R', 'F', 'E', 'R', 'I', 'F', 'D', 'K', 'W', 'T', 'C', 'G', 'L', 'M'], 'VWMPRFERIFDKWTCGLM', 0.9377846382963787, 2.3)
(['N', 'P', 'L', 'P', 'R', 'F', 'A', 'R', 'I', 'Y', 'T', 'K', 'K', 'W', 'Q', 'P'], 'NPLPRFARIYTKKWQP', 0.9592458198321689, 2.05)
(['Q', 'R', 'F', 'W', 'N', 'F', 'Y', 'T', 'Q', 'Y', 'W', 'G', 'H', 'D', 'F', 'I', 'N', 'E', 'F'], 'QRFWNFYTQYWGHDFINEF', 0.952156543884294, 2.05)
(['N', 'P', 'L', 'P', 'R', 'F', 'A', 'R', 'Q', 'Y', 'T', 'K', 'W', 'W', 'Q', 'P'], 'NPLPRFARQYTKWWQP', 0.9818505163583123, 1.55)
(['V', 'W', 'M', 'P', 'R', 'M', 'E', 'R', 'I', 'F', 'D', 'K', 'W', 'T', 'C', 'G', 'L', 'M'], 'VWMPRMERIFDKWTCGLM', 0.931582566366069, 2.44)
(['Q', 'R', 'L', 'E', 'L', 'M', 'E', 'R', 'I', 'F', 'D', 'K', 'W', 'T', 'C', 'G', 'L', 'M'], 'QRLELMERIFDKWTCGLM', 0.9795258736558395, 1.6)
(['Q', 'R', 'M', 'P', 'R', 'F', 'Y', 'R', 'I', 'F', 'T', 'K', 'K', 'W', 'F', 'I', 'N', 'E', 'F'], 'QRMPRFYRIFTKKWFINEF', 0.9483165508316579, 2.1)
(['K', 'W', 'M', 'P', 'R', 'F', 'A', 'R', 'I', 'T', 'W', 'G', 'H', 'D', 'F', 'I', 'N', 'E', 'F'], 'KWMPRFARITWGHDFINEF', 0.9357147561525847, 2.34)
(['N', 'P', 'L', 'P', 'R', 'F', 'A', 'R', 'I', 'F', 'D', 'K', 'W', 'T', 'C', 'G', 'L', 'M'], 'NPLPRFARIFDKWTCGLM', 0.983985992934927, 1.24)
(['V', 'W', 'M', 'P', 'R', 'F', 'A', 'R', 'I', 'Y', 'W', 'H', 'H', 'D', 'F', 'Q', 'R', 'M'], 'VWMPRFARIYWHHDFQRM', 0.8120544845873816, 3.06)
(['N', 'P', 'L', 'E', 'L', 'M', 'E', 'K', 'I', 'Y', 'W', 'H', 'K', 'W', 'F', 'Q'], 'NPLELMEKIYWHKWFQ', 0.9766803966694776, 2.04)
(['V', 'W', 'M', 'E', 'R', 'F', 'A', 'R', 'I', 'Y', 'T', 'K', 'K', 'W', 'Q', 'P'], 'VWMERFARIYTKKWQP', 0.8832620269761462, 2.69)
(['N', 'R', 'F', 'W', 'N', 'F', 'Y', 'N', 'I', 'Y', 'W', 'H', 'K', 'W', 'T', 'C'], 'NRFWNFYNIYWHKWTC', 0.948231307866216, 2.13)
"""

# Function call
points1 = extract_points(file_content1)
points2 = extract_points(file_content2)
points3 = extract_points(file_content3)
points4 = extract_points(file_content4)
points5 = extract_points(file_content5)

# Labels with names and areas
labels = [
    ("1", 2.7804, len(points1)),
    ("2", 2.4983, len(points2)),
    ("3", 2.3436, len(points3)),
    ("4", 2.37106, len(points4)),
    ("5", 2.9367, len(points5))
]

pareto_fronts = [points1, points2, points3, points4, points5]
# pareto_fronts = [points1]
visualize_convex_hull(pareto_fronts, labels)
