import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid

def extract_points(file_content):
    """
    Izvlači točke (x, y) iz datog sadržaja datoteke.
    
    :param file_content: Sadržaj datoteke kao string.
    :return: Lista točaka (x, y) kao tuple-ovi.
    """
    points = []
    for line in file_content.strip().split("\n"):
        # Uklanja zagrade i razdvaja elemente
        elements = eval(line.strip())
        x = elements[2]  # Treći element
        y = elements[3]  # Četvrti element
        points.append((x, y))
    return points


def visualize_convex_hull(pareto_fronts, labels):
    """
    Vizualizira Convex Hull krivulje za više Pareto fronti i dodaje oznake za svaki front.

    Parametri:
    pareto_fronts - lista listi, gdje svaka lista predstavlja Pareto front u obliku (Toksičnost, AMP vjerojatnost).
    labels - lista tupla, gdje svako tuple sadrži naziv skupa i njegovu vrijednost.
    """
    plt.figure(figsize=(10, 6))
    
    for idx, pareto_front in enumerate(pareto_fronts):
        # Extract (Toksičnost, AMP vjerojatnost) from the given pareto_front data
        x = np.array([point[1] for point in pareto_front])  # Toksičnost
        y = np.array([point[0] for point in pareto_front])  # AMP vjerojatnost

        # Sort points by x-values (Toksičnost)
        sorted_indices = np.argsort(x)
        sorted_x = x[sorted_indices]
        sorted_y = y[sorted_indices]

        # Add the point (0, 1) to the beginning of the Pareto front
        x_hull = np.concatenate(([0], sorted_x))  # Toksičnost
        y_hull = np.concatenate(([1], sorted_y))  # AMP vjerojatnost

        # Plot the convex hull without filling the area under the curve
        plt.plot(x_hull, y_hull, marker='o', linestyle='-', label=f'{labels[idx][0]} (CHArea: {labels[idx][1]}, BrojTočaka: {labels[idx][2]})')
    
    # Plot settings
    plt.title("Convex Hull Krivulje za više Pareto fronti")
    plt.xlabel("Toksičnost (ff_toxicity)")  # x-axis: Toksičnost
    plt.ylabel("Vjerojatnost postojanja AMP svojstva (ff_amp_probability)")  # y-axis: AMP vjerojatnost
    plt.xlim(0, max([np.array(x).max() for x in pareto_fronts])*1.1)  # Adjusting x-axis limit slightly to the right
    plt.ylim(0, 1)  # y-axis limited to 0-1 (AMP vjerojatnost)
    plt.grid(True)
    plt.legend(loc='lower left')
    plt.show()


file_content6 = """
(['Q', 'R', 'I', 'Y', 'L', 'V', 'L', 'D', 'Y', 'W', 'M', 'R', 'G', 'T', 'K', 'L', 'R', 'R'], 'QRIYLVLDYWMRGTKLRR', 0.663, 2.84)
(['Q', 'R', 'W', 'V', 'P', 'H', 'P', 'L', 'Q', 'Y', 'L', 'R', 'Q', 'T', 'I', 'H', 'H'], 'QRWVPHPLQYLRQTIHH', 0.99, 0.87)
(['S', 'P', 'W', 'E', 'I', 'Y', 'P', 'L', 'Q', 'K', 'T', 'P', 'K', 'K', 'L', 'P', 'K', 'M', 'P'], 'SPWEIYPLQKTPKKLPKMP', 0.99, 0.61)
(['Q', 'R', 'W', 'V', 'P', 'H', 'P', 'L', 'Q', 'Y', 'L', 'R', 'Q', 'F', 'Q', 'R', 'R'], 'QRWVPHPLQYLRQFQRR', 0.99, 0.91)
(['S', 'P', 'W', 'K', 'F', 'H', 'R', 'F', 'C', 'N', 'R', 'L', 'C', 'C', 'L', 'R', 'R'], 'SPWKFHRFCNRLCCLRR', 1.0, -1.8)
(['T', 'W', 'E', 'K', 'F', 'P', 'R', 'I', 'F', 'N', 'M', 'L', 'C', 'C', 'F', 'L', 'P', 'K'], 'TWEKFPRIFNMLCCFLPK', 1.0, -0.03)
(['S', 'P', 'W', 'E', 'G', 'V', 'T', 'K', 'H', 'K', 'T', 'P', 'K', 'K', 'L', 'P', 'K', 'M', 'P'], 'SPWEGVTKHKTPKKLPKMP', 0.99, 1.2)
(['Q', 'R', 'W', 'V', 'P', 'R', 'I', 'F', 'Y', 'W', 'M', 'P', 'K', 'I', 'F', 'R', 'R', 'L', 'T'], 'QRWVPRIFYWMPKIFRRLT', 0.8415, 2.72)
(['S', 'Y', 'P', 'H', 'H', 'K', 'I', 'F', 'Y', 'W', 'M', 'P', 'K', 'I', 'F', 'S', 'H'], 'SYPHHKIFYWMPKIFSH', 0.98, 2.16)
(['S', 'P', 'W', 'V', 'P', 'H', 'P', 'L', 'Q', 'Y', 'L', 'R', 'Q', 'T', 'I', 'H', 'H'], 'SPWVPHPLQYLRQTIHH', 0.99, 0.62)
(['H', 'Y', 'P', 'H', 'H', 'K', 'T', 'K', 'Y', 'W', 'M', 'R', 'T', 'K', 'L', 'P', 'R'], 'HYPHHKTKYWMRTKLPR', 0.98, 2.2)
(['Q', 'R', 'I', 'Y', 'L', 'V', 'L', 'D', 'Y', 'W', 'M', 'P', 'K', 'K', 'L', 'P', 'K', 'M', 'P'], 'QRIYLVLDYWMPKKLPKMP', 0.92, 2.35)
(['Q', 'P', 'W', 'K', 'G', 'V', 'T', 'K', 'H', 'K', 'T', 'P', 'K', 'K', 'L', 'P', 'K', 'M', 'P'], 'QPWKGVTKHKTPKKLPKMP', 0.99, 1.44)
(['H', 'Y', 'P', 'H', 'H', 'K', 'Q', 'Y', 'Q', 'K', 'T', 'P', 'K', 'K', 'L', 'P', 'K', 'M', 'P'], 'HYPHHKQYQKTPKKLPKMP', 0.99, 0.73)
(['H', 'R', 'I', 'Y', 'L', 'R', 'I', 'F', 'N', 'M', 'L', 'C', 'C', 'F', 'T', 'F', 'P', 'N', 'H'], 'HRIYLRIFNMLCCFTFPNH', 0.99, 0.58)
(['S', 'P', 'W', 'K', 'F', 'H', 'R', 'F', 'Q', 'Y', 'L', 'R', 'Q', 'F', 'Q', 'R', 'R'], 'SPWKFHRFQYLRQFQRR', 0.99, 0.43)
(['H', 'R', 'W', 'V', 'P', 'R', 'I', 'F', 'N', 'M', 'L', 'C', 'C', 'F', 'I', 'H', 'H'], 'HRWVPRIFNMLCCFIHH', 1.0, 0.32)
(['Q', 'R', 'W', 'V', 'P', 'R', 'I', 'F', 'N', 'M', 'L', 'C', 'C', 'F', 'I', 'H', 'H'], 'QRWVPRIFNMLCCFIHH', 0.99, 0.51)
(['H', 'Y', 'P', 'H', 'H', 'K', 'Q', 'Y', 'Y', 'T', 'E', 'L', 'K', 'K', 'L', 'S', 'H'], 'HYPHHKQYYTELKKLSH', 0.99, 1.45)
(['Q', 'R', 'W', 'V', 'P', 'R', 'I', 'F', 'Y', 'W', 'M', 'P', 'K', 'I', 'F', 'R', 'R', 'M', 'P'], 'QRWVPRIFYWMPKIFRRMP', 0.8415, 2.82)
(['S', 'W', 'E', 'K', 'F', 'P', 'R', 'I', 'F', 'N', 'M', 'L', 'C', 'C', 'F', 'L', 'P', 'K'], 'SWEKFPRIFNMLCCFLPK', 1.0, 0.11)
(['Q', 'R', 'W', 'V', 'P', 'H', 'I', 'F', 'Y', 'W', 'M', 'P', 'K', 'I', 'F', 'R', 'R', 'L', 'T'], 'QRWVPHIFYWMPKIFRRLT', 0.8415, 2.4)
"""

file_content7 = """
(['Q', 'Q', 'W', 'N', 'Q', 'W', 'T', 'K', 'I', 'H', 'H', 'C'], 'QQWNQWTKIHHC', 0.99, 1.0)
(['H', 'P', 'W', 'N', 'Q', 'W', 'S', 'Q', 'R', 'H', 'K', 'V', 'V', 'V', 'G', 'R', 'I', 'W', 'Q'], 'HPWNQWSQRHKVVVGRIWQ', 0.99, 0.96)
(['E', 'A', 'L', 'W', 'R', 'R', 'T', 'K', 'I', 'F', 'K', 'V', 'V', 'V', 'G', 'R', 'I', 'W', 'Q'], 'EALWRRTKIFKVVVGRIWQ', 0.99, 1.35)
(['I', 'Y', 'M', 'T', 'F', 'R', 'T', 'K', 'I', 'L', 'A', 'V', 'F', 'I', 'Y', 'A', 'I', 'K'], 'IYMTFRTKILAVFIYAIK', 0.4, 2.6)
(['H', 'P', 'W', 'N', 'R', 'W', 'S', 'K', 'R', 'H', 'H', 'C'], 'HPWNRWSKRHHC', 1.0, 0.16)
(['I', 'Y', 'M', 'T', 'F', 'R', 'T', 'K', 'I', 'F', 'K', 'V', 'F', 'I', 'Y', 'A', 'F', 'I', 'T'], 'IYMTFRTKIFKVFIYAFIT', 0.5780000000000001, 2.55)
(['E', 'A', 'L', 'T', 'F', 'W', 'K', 'K', 'I', 'L', 'A', 'V', 'F', 'I', 'Y', 'A', 'F', 'I', 'T'], 'EALTFWKKILAVFIYAFIT', 0.98, 1.99)
(['H', 'P', 'W', 'N', 'Q', 'W', 'T', 'K', 'I', 'H', 'H', 'V', 'V', 'V', 'G', 'R', 'I', 'W', 'Q'], 'HPWNQWTKIHHVVVGRIWQ', 0.99, 1.0)
(['H', 'P', 'W', 'N', 'R', 'W', 'T', 'K', 'I', 'H', 'H', 'V', 'V', 'V', 'G', 'R', 'I', 'W', 'Q'], 'HPWNRWTKIHHVVVGRIWQ', 0.99, 0.99)
(['H', 'P', 'W', 'N', 'R', 'W', 'S', 'Q', 'I', 'F', 'K', 'V', 'V', 'V', 'Y', 'T', 'I', 'I', 'T'], 'HPWNRWSQIFKVVVYTIIT', 0.99, 1.1)
(['Q', 'Y', 'L', 'W', 'Q', 'W', 'S', 'Q', 'I', 'F', 'K', 'V', 'V', 'V', 'G', 'R', 'I', 'W', 'Q'], 'QYLWQWSQIFKVVVGRIWQ', 0.99, 1.1)
(['E', 'A', 'L', 'T', 'F', 'W', 'K', 'K', 'I', 'F', 'K', 'I', 'F', 'K', 'I', 'Y', 'A', 'I', 'K'], 'EALTFWKKIFKIFKIYAIK', 0.99, 1.61)
(['Q', 'Q', 'W', 'W', 'Q', 'W', 'S', 'Q', 'I', 'F', 'K', 'V', 'V', 'V', 'G', 'R', 'I', 'W', 'Q'], 'QQWWQWSQIFKVVVGRIWQ', 0.99, 1.01)
(['Q', 'Q', 'W', 'N', 'F', 'W', 'K', 'K', 'I', 'F', 'K', 'I', 'F', 'K', 'I', 'Y', 'A', 'I', 'K'], 'QQWNFWKKIFKIFKIYAIK', 0.99, 1.78)
(['I', 'Y', 'M', 'T', 'F', 'R', 'T', 'K', 'I', 'F', 'K', 'V', 'F', 'T', 'V', 'A', 'I', 'T'], 'IYMTFRTKIFKVFTVAIT', 0.408, 2.6)
(['E', 'A', 'L', 'T', 'F', 'R', 'T', 'K', 'I', 'F', 'K', 'I', 'F', 'I', 'Y', 'T', 'I', 'I', 'T'], 'EALTFRTKIFKIFIYTIIT', 0.97, 2.03)
(['Q', 'Q', 'W', 'N', 'Q', 'W', 'T', 'K', 'R', 'H', 'K', 'V', 'V', 'V', 'G', 'R', 'I', 'W', 'Q'], 'QQWNQWTKRHKVVVGRIWQ', 0.99, 1.4)
(['E', 'A', 'W', 'N', 'Q', 'W', 'T', 'K', 'I', 'H', 'K', 'I', 'V', 'I', 'G', 'R', 'I', 'W', 'Q'], 'EAWNQWTKIHKIVIGRIWQ', 0.99, 1.54)
(['H', 'P', 'W', 'N', 'R', 'W', 'S', 'Q', 'I', 'F', 'K', 'V', 'V', 'V', 'Y', 'T', 'I', 'K'], 'HPWNRWSQIFKVVVYTIK', 0.99, 1.06)
(['H', 'P', 'W', 'N', 'Q', 'W', 'S', 'Q', 'R', 'H', 'H', 'C'], 'HPWNQWSQRHHC', 0.99, 0.23)
(['H', 'P', 'W', 'N', 'R', 'W', 'S', 'Q', 'Q', 'H', 'H', 'C'], 'HPWNRWSQQHHC', 0.99, 0.4)
(['Q', 'Q', 'W', 'N', 'Q', 'W', 'T', 'Q', 'R', 'H', 'H', 'C'], 'QQWNQWTQRHHC', 0.99, 0.79)
(['H', 'P', 'W', 'N', 'Q', 'W', 'T', 'K', 'I', 'H', 'H', 'C'], 'HPWNQWTKIHHC', 0.99, 0.55)
(['H', 'P', 'W', 'N', 'Q', 'W', 'S', 'Q', 'R', 'H', 'K', 'C'], 'HPWNQWSQRHKC', 0.99, 0.55)
(['H', 'P', 'W', 'N', 'R', 'W', 'S', 'Q', 'I', 'F', 'K', 'C'], 'HPWNRWSQIFKC', 0.99, 0.45)
(['H', 'P', 'W', 'N', 'R', 'W', 'S', 'Q', 'R', 'H', 'H', 'C'], 'HPWNRWSQRHHC', 0.99, 0.3)
(['H', 'P', 'W', 'P', 'N', 'Q', 'W', 'T', 'K', 'I', 'H', 'H', 'C'], 'HPWPNQWTKIHHC', 0.99, 0.27)
(['E', 'A', 'L', 'N', 'Q', 'W', 'T', 'K', 'I', 'H', 'K', 'I', 'F', 'I', 'Y', 'A', 'I', 'K'], 'EALNQWTKIHKIFIYAIK', 0.97, 2.17)
(['Q', 'Q', 'W', 'N', 'F', 'W', 'K', 'K', 'I', 'F', 'K', 'I', 'F', 'I', 'Y', 'A', 'F', 'I', 'T'], 'QQWNFWKKIFKIFIYAFIT', 0.99, 1.99)
(['H', 'P', 'W', 'N', 'R', 'W', 'T', 'K', 'R', 'H', 'K', 'V', 'V', 'G', 'R', 'I', 'W', 'Q'], 'HPWNRWTKRHKVVGRIWQ', 0.99, 0.98)
(['H', 'P', 'W', 'S', 'T', 'F', 'R', 'T', 'K', 'I', 'F', 'K', 'I', 'F', 'I', 'Y', 'T', 'I', 'I', 'T'], 'HPWSTFRTKIFKIFIYTIIT', 0.99, 1.69)
(['I', 'Y', 'M', 'T', 'F', 'R', 'T', 'K', 'I', 'F', 'A', 'V', 'F', 'I', 'Y', 'A', 'F', 'I', 'T'], 'IYMTFRTKIFAVFIYAFIT', 0.306, 2.67)
(['H', 'P', 'W', 'N', 'R', 'W', 'T', 'K', 'R', 'H', 'K', 'V', 'V', 'V', 'G', 'R', 'I', 'W', 'Q'], 'HPWNRWTKRHKVVVGRIWQ', 0.99, 1.0)
(['E', 'A', 'W', 'N', 'F', 'R', 'T', 'K', 'E', 'L', 'A', 'V', 'F', 'I', 'Y', 'A', 'F', 'I', 'T'], 'EAWNFRTKELAVFIYAFIT', 0.7395, 2.48)
(['Q', 'Q', 'W', 'N', 'F', 'R', 'T', 'K', 'E', 'L', 'A', 'V', 'F', 'I', 'Y', 'A', 'F', 'I', 'T'], 'QQWNFRTKELAVFIYAFIT', 0.765, 2.39)
(['H', 'Y', 'M', 'T', 'F', 'R', 'T', 'K', 'I', 'F', 'K', 'V', 'F', 'I', 'Y', 'A', 'F', 'I', 'T'], 'HYMTFRTKIFKVFIYAFIT', 0.816, 2.36)
(['H', 'P', 'W', 'W', 'R', 'R', 'T', 'K', 'I', 'F', 'K', 'V', 'V', 'V', 'G', 'R', 'I', 'W', 'Q'], 'HPWWRRTKIFKVVVGRIWQ', 0.99, 1.02)
(['I', 'Y', 'M', 'T', 'F', 'R', 'T', 'K', 'I', 'L', 'A', 'V', 'F', 'I', 'Y', 'A', 'F', 'I', 'T'], 'IYMTFRTKILAVFIYAFIT', 0.2635, 2.67)
(['Q', 'Y', 'L', 'W', 'Q', 'W', 'S', 'Q', 'I', 'F', 'K', 'V', 'V', 'V', 'G', 'R', 'F', 'I', 'T'], 'QYLWQWSQIFKVVVGRFIT', 0.99, 1.2)
(['Q', 'P', 'W', 'N', 'R', 'W', 'S', 'Q', 'I', 'F', 'K', 'V', 'V', 'V', 'Y', 'T', 'I', 'I', 'T'], 'QPWNRWSQIFKVVVYTIIT', 0.99, 1.55)
(['Q', 'Q', 'L', 'T', 'F', 'W', 'K', 'K', 'I', 'L', 'A', 'V', 'F', 'I', 'Y', 'A', 'F', 'I', 'T'], 'QQLTFWKKILAVFIYAFIT', 0.97, 2.19)
(['Q', 'Q', 'W', 'N', 'F', 'W', 'T', 'K', 'E', 'L', 'A', 'V', 'F', 'I', 'Y', 'A', 'I', 'K'], 'QQWNFWTKELAVFIYAIK', 0.94, 2.32)
(['H', 'P', 'W', 'N', 'R', 'W', 'S', 'Q', 'I', 'F', 'K', 'V', 'V', 'V', 'Y', 'T', 'I', 'W', 'Q'], 'HPWNRWSQIFKVVVYTIWQ', 0.99, 0.87)
"""

file_content8= """
(['H', 'N', 'I', 'Y', 'R', 'W', 'P', 'R', 'L', 'H', 'D', 'H', 'W', 'I', 'K'], 'HNIYRWPRLHDHWIK', 0.99, 1.27)
(['A', 'Y', 'V', 'Y', 'A', 'V', 'P', 'R', 'L', 'M', 'S', 'H', 'S', 'W', 'G', 'E', 'Q'], 'AYVYAVPRLMSHSWGEQ', 0.8075, 2.3)
(['A', 'Y', 'V', 'Y', 'R', 'V', 'P', 'R', 'L', 'M', 'S', 'H', 'S', 'W', 'G', 'E', 'Q'], 'AYVYRVPRLMSHSWGEQ', 0.833, 2.23)
(['A', 'Y', 'V', 'K', 'Q', 'W', 'P', 'R', 'V', 'C', 'V', 'K', 'I', 'L', 'C'], 'AYVKQWPRVCVKILC', 0.99, 0.89)
(['H', 'N', 'I', 'K', 'R', 'W', 'P', 'R', 'L', 'H', 'D', 'K', 'I', 'L', 'G', 'E', 'Q'], 'HNIKRWPRLHDKILGEQ', 0.99, 1.54)
(['S', 'N', 'L', 'K', 'Q', 'V', 'E', 'R', 'I', 'V', 'C', 'C', 'W', 'G', 'K'], 'SNLKQVERIVCCWGK', 1.0, -0.21)
(['A', 'V', 'Y', 'A', 'R', 'W', 'P', 'R', 'K', 'H', 'V', 'K', 'I', 'L', 'C'], 'AVYARWPRKHVKILC', 0.99, 1.61)
(['S', 'N', 'I', 'A', 'R', 'W', 'P', 'R', 'L', 'M', 'S', 'C', 'C', 'K', 'K'], 'SNIARWPRLMSCCKK', 1.0, -0.25)
(['H', 'N', 'I', 'Y', 'R', 'W', 'P', 'R', 'L', 'H', 'V', 'K', 'I', 'L', 'G', 'E', 'W'], 'HNIYRWPRLHVKILGEW', 0.99, 2.02)
(['H', 'N', 'I', 'Y', 'R', 'W', 'P', 'G', 'L', 'M', 'C', 'C', 'C', 'L', 'C'], 'HNIYRWPGLMCCCLC', 1.0, -1.73)
(['A', 'Y', 'V', 'Y', 'R', 'V', 'P', 'R', 'L', 'M', 'S', 'H', 'S', 'W', 'G', 'E', 'W'], 'AYVYRVPRLMSHSWGEW', 0.833, 2.19)
(['A', 'V', 'Y', 'A', 'R', 'W', 'P', 'G', 'L', 'M', 'C', 'C', 'C', 'L', 'C'], 'AVYARWPGLMCCCLC', 1.0, -1.83)
(['A', 'Y', 'V', 'K', 'Q', 'W', 'P', 'R', 'V', 'V', 'K', 'C', 'I', 'L', 'C'], 'AYVKQWPRVVKCILC', 1.0, 0.46)
(['H', 'N', 'I', 'Y', 'R', 'W', 'Q', 'R', 'L', 'M', 'S', 'H', 'S', 'W', 'G', 'E', 'Q'], 'HNIYRWQRLMSHSWGEQ', 0.99, 1.97)
(['H', 'Y', 'V', 'Y', 'R', 'V', 'P', 'R', 'L', 'M', 'S', 'P', 'S', 'W', 'G', 'E', 'Q'], 'HYVYRVPRLMSPSWGEQ', 0.98, 2.16)
(['A', 'Y', 'V', 'K', 'Q', 'V', 'E', 'R', 'I', 'V', 'C', 'C', 'W', 'G', 'K'], 'AYVKQVERIVCCWGK', 1.0, -0.2)
(['Y', 'L', 'E', 'K', 'A', 'V', 'P', 'R', 'V', 'V', 'K', 'C', 'I', 'L', 'C'], 'YLEKAVPRVVKCILC', 0.99, 1.26)
(['S', 'N', 'L', 'K', 'Q', 'V', 'E', 'R', 'I', 'V', 'C', 'C', 'C', 'L', 'C'], 'SNLKQVERIVCCCLC', 1.0, -1.47)
(['H', 'N', 'I', 'Y', 'R', 'W', 'Q', 'R', 'L', 'M', 'S', 'H', 'W', 'I', 'K'], 'HNIYRWQRLMSHWIK', 0.99, 1.29)
(['H', 'N', 'I', 'Y', 'R', 'W', 'P', 'R', 'L', 'H', 'V', 'K', 'I', 'L', 'G', 'E', 'Q'], 'HNIYRWPRLHVKILGEQ', 0.98, 2.04)
(['Y', 'L', 'E', 'K', 'A', 'V', 'E', 'R', 'L', 'M', 'S', 'H', 'S', 'W', 'G', 'E', 'W'], 'YLEKAVERLMSHSWGEW', 0.95, 2.17)
(['Y', 'L', 'E', 'K', 'Q', 'W', 'P', 'R', 'V', 'V', 'K', 'C', 'I', 'L', 'C'], 'YLEKQWPRVVKCILC', 0.99, 0.7)
(['S', 'N', 'L', 'K', 'Q', 'W', 'P', 'R', 'V', 'V', 'K', 'C', 'I', 'L', 'C'], 'SNLKQWPRVVKCILC', 1.0, 0.52)
(['H', 'N', 'I', 'K', 'R', 'W', 'P', 'R', 'L', 'M', 'S', 'H', 'S', 'W', 'G', 'E', 'W'], 'HNIKRWPRLMSHSWGEW', 0.99, 1.67)
"""

file_content9 = """
(['T', 'K', 'I', 'F', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W'], 'TKIFYMPQLVKNIHCQW', 0.99, 1.59)
(['D', 'I', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'DIYARMPQLVKNIHSI', 0.98, 2.16)
(['D', 'I', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'DIYARMPQLVKNIHSQD', 0.97, 2.32)
(['T', 'K', 'W', 'G', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'TKWGYMPQLVKNIHSI', 0.99, 1.8)
(['T', 'K', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'TKYARMPQLVKNIHSQD', 0.98, 2.23)
(['T', 'K', 'I', 'F', 'R', 'M', 'P', 'Q', 'L', 'D', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'TKIFRMPQLDKNIHSQD', 0.91, 2.56)
(['A', 'R', 'W', 'G', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W', 'D', 'M'], 'ARWGYMPQLVKNIHCQWDM', 1.0, 0.84)
(['T', 'K', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'TKYARMPQLVKNIHSI', 0.99, 2.05)
(['A', 'R', 'W', 'G', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'ARWGYMPQLVKNIHSI', 0.99, 1.82)
(['S', 'R', 'W', 'L', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'SRWLRMPQLVKNIHSI', 0.99, 1.63)
(['T', 'K', 'I', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'TKIFRMPQLVKNIHSI', 0.98, 2.32)
(['T', 'K', 'I', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W', 'D'], 'TKIFRMPQLVKNIHCQWD', 0.99, 1.49)
(['T', 'K', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W', 'D', 'M'], 'TKYARMPQLVKNIHCQWDM', 1.0, 1.07)
(['T', 'K', 'I', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'TKIFRMPQLVKNIHSQD', 0.97, 2.51)
(['A', 'R', 'W', 'G', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W'], 'ARWGYMPQLVKNIHCQW', 1.0, 1.12)
(['T', 'K', 'W', 'G', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W', 'D', 'M'], 'TKWGYMPQLVKNIHCQWDM', 1.0, 0.84)
(['D', 'I', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'W', 'D', 'M'], 'DIYARMPQLVKNIHSQWDM', 0.99, 1.67)
(['T', 'K', 'I', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W'], 'TKIFRMPQLVKNIHCQW', 0.99, 1.67)
(['D', 'I', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W'], 'DIYARMPQLVKNIHCQW', 0.99, 1.45)
(['S', 'R', 'W', 'L', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'SRWLRMPQLVKNIHSQD', 0.99, 1.84)
(['K', 'K', 'I', 'F', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'I'], 'KKIFYMPQLVKNIHCI', 0.99, 1.44)
(['D', 'K', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'DKYARMPQLVKNIHSQD', 0.99, 1.92)
(['T', 'I', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'TIYARMPQLVKNIHSI', 0.98, 2.12)
(['D', 'K', 'I', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'DKIFRMPQLVKNIHSI', 0.99, 1.97)
(['T', 'K', 'S', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'TKSFRMPQLVKNIHSI', 0.98, 2.17)
(['T', 'K', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W'], 'TKYARMPQLVKNIHCQW', 1.0, 1.36)
(['T', 'K', 'S', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'TKSFRMPQLVKNIHSQD', 0.97, 2.36)
(['K', 'K', 'I', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'KKIFRMPQLVKNIHSI', 0.98, 2.08)
(['A', 'R', 'W', 'G', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'ARWGRMPQLVKNIHSI', 0.99, 1.8)
(['T', 'K', 'S', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W'], 'TKSFRMPQLVKNIHCQW', 0.99, 1.49)
(['T', 'K', 'Y', 'L', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'TKYLRMPQLVKNIHSQD', 0.98, 2.27)
(['T', 'K', 'W', 'G', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'I'], 'TKWGYMPQLVKNIHCI', 1.0, 1.22)
(['T', 'K', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q'], 'TKYARMPQLVKNIHCQ', 0.99, 1.5)
(['A', 'R', 'W', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'ARWFRMPQLVKNIHSQD', 0.98, 2.19)
(['D', 'K', 'I', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'I'], 'DKIFRMPQLVKNIHCI', 1.0, 1.4)
(['D', 'I', 'Y', 'L', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'DIYLRMPQLVKNIHSQD', 0.97, 2.37)
(['T', 'K', 'W', 'G', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W'], 'TKWGYMPQLVKNIHCQW', 1.0, 1.11)
(['A', 'R', 'W', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'I'], 'ARWARMPQLVKNIHSI', 0.99, 1.88)
(['D', 'K', 'I', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'DKIFRMPQLVKNIHSQD', 0.98, 2.17)
(['T', 'K', 'S', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'I'], 'TKSFRMPQLVKNIHCI', 0.99, 1.59)
(['A', 'R', 'W', 'G', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'D'], 'ARWGYMPQLVKNIHCQD', 0.99, 1.47)
(['T', 'K', 'I', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'I'], 'TKIFRMPQLVKNIHCI', 0.99, 1.76)
(['A', 'R', 'W', 'G', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'I'], 'ARWGYMPQLVKNIHCI', 1.0, 1.24)
(['T', 'I', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W'], 'TIYARMPQLVKNIHCQW', 0.99, 1.43)
(['A', 'R', 'W', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'W'], 'ARWARMPQLVKNIHCQW', 1.0, 1.24)
(['D', 'K', 'I', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'D'], 'DKIFRMPQLVKNIHCQD', 0.99, 1.66)
(['A', 'R', 'W', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'ARWARMPQLVKNIHSQD', 0.99, 2.07)
(['T', 'K', 'I', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'D'], 'TKIARMPQLVKNIHSQD', 0.98, 2.28)
(['T', 'K', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'D'], 'TKYARMPQLVKNIHCQD', 0.99, 1.69)
(['T', 'I', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q', 'W'], 'TIYARMPQLVKNIHSQW', 0.99, 1.98)
(['D', 'I', 'Y', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'I'], 'DIYFRMPQLVKNIHCI', 0.99, 1.6)
(['T', 'K', 'S', 'F', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q'], 'TKSFRMPQLVKNIHSQ', 0.98, 2.19)
(['T', 'K', 'W', 'G', 'Y', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q', 'D'], 'TKWGYMPQLVKNIHCQD', 0.99, 1.44)
(['T', 'I', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'S', 'Q'], 'TIYARMPQLVKNIHSQ', 0.98, 2.14)
(['D', 'I', 'Y', 'A', 'R', 'M', 'P', 'Q', 'L', 'V', 'K', 'N', 'I', 'H', 'C', 'Q'], 'DIYARMPQLVKNIHCQ', 0.99, 1.6)
"""

file_content10 = """
(['A', 'V', 'W', 'A', 'H', 'A', 'H', 'K', 'L', 'E', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVWAHAHKLERRIFEK', 0.99, 2.2)
(['A', 'V', 'Y', 'W', 'A', 'A', 'Q', 'H', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAAQHHKIERIFQK', 0.98, 2.36)
(['A', 'V', 'Y', 'W', 'A', 'H', 'H', 'K', 'I', 'L', 'E', 'R', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHHKILERRIFQK', 0.97, 2.63)
(['A', 'V', 'Y', 'W', 'A', 'H', 'H', 'K', 'I', 'L', 'E', 'R', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHHKILERRIFQK', 0.97, 2.63)
(['A', 'V', 'Y', 'W', 'A', 'H', 'Q', 'H', 'K', 'K', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHQHKKIERIFQK', 0.99, 2.28)
(['A', 'V', 'Y', 'W', 'A', 'H', 'E', 'H', 'K', 'K', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHEHKKIERIFQK', 0.99, 2.23)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHAHKIERRIFQK', 0.99, 2.22)
(['A', 'V', 'Y', 'W', 'A', 'M', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'E', 'K'], 'AVYWAMAQHKIERIFEK', 0.98, 2.37)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'Q', 'H', 'K', 'I', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHAQHKIRRIFEK', 0.99, 1.91)
(['A', 'V', 'Y', 'W', 'A', 'M', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'E', 'K'], 'AVYWAMAQHKIERIFEK', 0.98, 2.37)
(['A', 'V', 'Y', 'W', 'A', 'H', 'Q', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHQHKIERRIFQK', 0.98, 2.39)
(['A', 'V', 'Y', 'W', 'A', 'H', 'E', 'H', 'K', 'K', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHEHKKIERIFQK', 0.99, 2.23)
(['A', 'V', 'Y', 'W', 'A', 'H', 'Q', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHQHKIERRIFEK', 0.98, 2.38)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHAHKIERRIFEK', 0.99, 2.24)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'F', 'E', 'W'], 'AVYWAHAHKIERRIFEW', 0.99, 2.26)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHAQHKIERIFQK', 0.99, 2.2)
(['A', 'V', 'Y', 'W', 'A', 'H', 'Q', 'H', 'K', 'K', 'I', 'E', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHQHKKIERIFEK', 0.99, 2.27)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHAQHKIERIFEK', 0.99, 2.19)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'F', 'E', 'W'], 'AVYWAHAHKIERRIFEW', 0.99, 2.26)
(['A', 'V', 'Y', 'W', 'A', 'H', 'H', 'K', 'K', 'K', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHHKKKIERIFQK', 0.99, 2.24)
(['A', 'V', 'Y', 'W', 'A', 'H', 'Q', 'H', 'K', 'I', 'E', 'H', 'Y', 'I', 'R', 'H', 'I', 'P', 'M'], 'AVYWAHQHKIEHYIRHIPM', 0.99, 1.06)
(['A', 'V', 'Y', 'W', 'A', 'H', 'E', 'V', 'G', 'H', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHEVGHIERIFQK', 0.99, 2.22)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'F', 'E', 'H', 'K'], 'AVYWAHAHKIIERIFEHK', 0.99, 2.06)
(['A', 'V', 'Y', 'W', 'A', 'H', 'Q', 'H', 'K', 'K', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHQHKKIERIFQK', 0.99, 2.28)
(['A', 'V', 'Y', 'W', 'A', 'A', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'E', 'K'], 'AVYWAAAQHKIERIFEK', 0.99, 2.3)
(['A', 'V', 'Y', 'W', 'A', 'A', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'R', 'H', 'I', 'P'], 'AVYWAAAHKIIERIRHIP', 0.99, 1.9)
(['A', 'V', 'Y', 'W', 'A', 'H', 'H', 'K', 'I', 'L', 'E', 'R', 'I', 'F', 'Q'], 'AVYWAHHKILERIFQ', 0.97, 2.64)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'F', 'Q', 'I', 'P', 'M'], 'AVYWAHAHKIIERIFQIPM', 0.99, 1.89)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHAHKIIERIFQK', 0.99, 2.04)
(['A', 'V', 'W', 'A', 'H', 'A', 'H', 'K', 'L', 'E', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVWAHAHKLERRIFEK', 0.99, 2.2)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHAHKIIERIFEK', 0.99, 2.06)
(['A', 'V', 'Y', 'W', 'A', 'A', 'Q', 'H', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAAQHHKIERIFQK', 0.98, 2.36)
(['A', 'V', 'Y', 'W', 'A', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'R', 'H', 'I', 'P'], 'AVYWAAQHKIERRIRHIP', 0.99, 2.09)
(['A', 'V', 'Y', 'W', 'A', 'A', 'Q', 'H', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'E', 'K'], 'AVYWAAQHHKIERIFEK', 0.99, 2.33)
(['A', 'V', 'Y', 'W', 'A', 'A', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'E', 'K'], 'AVYWAAAQHKIERIFEK', 0.99, 2.3)
(['A', 'V', 'Y', 'W', 'A', 'A', 'Q', 'H', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'E', 'K'], 'AVYWAAQHHKIERIFEK', 0.99, 2.33)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'R', 'H', 'I', 'P', 'M'], 'AVYWAHAHKIIERIRHIPM', 0.99, 1.62)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'R', 'E', 'K'], 'AVYWAHAHKIIERIREK', 0.99, 1.67)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'R', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHAHKIIRRIFQK', 0.99, 1.74)
(['A', 'V', 'Y', 'W', 'A', 'H', 'Q', 'H', 'K', 'I', 'E', 'H', 'Y', 'I', 'R', 'H', 'I', 'P', 'M'], 'AVYWAHQHKIEHYIRHIPM', 0.99, 1.06)
(['A', 'V', 'Y', 'W', 'A', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVYWAAQHKIERRIFEK', 0.98, 2.45)
(['A', 'V', 'Y', 'W', 'A', 'H', 'Q', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHQHKIERRIFQK', 0.98, 2.39)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'R', 'E', 'K'], 'AVYWAHAHKIIERIREK', 0.99, 1.67)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'R', 'H', 'I', 'P'], 'AVYWAHAHKIIERIRHIP', 0.99, 1.73)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'Q', 'K', 'I', 'E', 'H', 'Y', 'I', 'R', 'H', 'I', 'P', 'M'], 'AVYWAHAQKIEHYIRHIPM', 0.99, 0.72)
(['A', 'V', 'Y', 'W', 'A', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVYWAAQHKIERRIFEK', 0.98, 2.45)
(['A', 'V', 'Y', 'W', 'A', 'H', 'H', 'K', 'I', 'L', 'E', 'R', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHHKILERRIFQK', 0.97, 2.63)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'R', 'H', 'I', 'P', 'M'], 'AVYWAHAHKIIERIRHIPM', 0.99, 1.62)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHAHKIIRRIFEK', 0.99, 1.78)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHAQHKIERIFEK', 0.99, 2.19)
(['A', 'V', 'Y', 'W', 'A', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'R', 'H', 'I', 'P'], 'AVYWAAQHKIERRIRHIP', 0.99, 2.09)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'R', 'R', 'I', 'R', 'H', 'I', 'P', 'M'], 'AVYWAHAHKIIRRIRHIPM', 0.99, 1.22)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'F', 'E', 'H'], 'AVYWAHAHKIIERIFEH', 0.99, 1.88)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHAHKIIERIFQK', 0.99, 2.04)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'Q', 'H', 'K', 'I', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHAQHKIRRIFEK', 0.99, 1.91)
(['A', 'V', 'Y', 'W', 'A', 'H', 'H', 'K', 'K', 'I', 'E', 'H', 'Y', 'I', 'R', 'H', 'I', 'P', 'M'], 'AVYWAHHKKIEHYIRHIPM', 0.99, 1.11)
(['A', 'V', 'Y', 'W', 'A', 'A', 'Q', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'F', 'Q'], 'AVYWAAQHKIERRIFQ', 0.98, 2.54)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'E', 'H', 'Y', 'I', 'R', 'H', 'I', 'P', 'M'], 'AVYWAHAHKIEHYIRHIPM', 0.99, 1.04)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'R', 'R', 'I', 'R', 'H', 'I', 'P', 'M'], 'AVYWAHAHKIIRRIRHIPM', 0.99, 1.22)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'Q', 'K', 'I', 'E', 'H', 'Y', 'I', 'R', 'H', 'I', 'P'], 'AVYWAHAQKIEHYIRHIP', 0.99, 0.8)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'E', 'R', 'I', 'R', 'E', 'I', 'P'], 'AVYWAHAHKIIERIREIP', 0.99, 1.53)
(['A', 'V', 'Y', 'W', 'A', 'H', 'Q', 'H', 'K', 'I', 'E', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHQHKIERRIFEK', 0.98, 2.38)
(['A', 'V', 'Y', 'W', 'A', 'A', 'Q', 'H', 'H', 'K', 'I', 'E', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAAQHHKIERIFQK', 0.98, 2.36)
(['A', 'V', 'Y', 'W', 'A', 'H', 'H', 'K', 'I', 'L', 'E', 'R', 'R', 'I', 'F', 'Q', 'K'], 'AVYWAHHKILERRIFQK', 0.97, 2.63)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'H', 'K', 'I', 'I', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHAHKIIRRIFEK', 0.99, 1.78)
(['A', 'V', 'Y', 'W', 'A', 'H', 'H', 'K', 'I', 'L', 'E', 'R', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHHKILERRIFEK', 0.97, 2.65)
(['A', 'V', 'Y', 'W', 'A', 'H', 'H', 'K', 'I', 'L', 'E', 'R', 'R', 'I', 'F', 'Q'], 'AVYWAHHKILERRIFQ', 0.96, 2.73)
(['A', 'V', 'Y', 'W', 'A', 'H', 'A', 'Q', 'K', 'I', 'E', 'H', 'Y', 'I', 'R', 'H', 'I', 'P', 'M'], 'AVYWAHAQKIEHYIRHIPM', 0.99, 0.72)
(['A', 'V', 'Y', 'W', 'A', 'H', 'Q', 'H', 'K', 'K', 'I', 'E', 'R', 'I', 'F', 'E', 'K'], 'AVYWAHQHKKIERIFEK', 0.99, 2.27)
(['A', 'V', 'Y', 'W', 'A', 'H', 'H', 'K', 'I', 'L', 'E', 'R', 'R', 'I', 'F', 'Q'], 'AVYWAHHKILERRIFQ', 0.96, 2.73)
"""
# Primjer sadržaja datoteke
file_content1 = """
(['T', 'L', 'P', 'R', 'R', 'I', 'Y', 'T', 'F', 'S', 'R', 'I', 'Y', 'A', 'F', 'Y', 'R'], 'TLPRRIYTFSRIYAFYR', 0.8105484692451637, 2.78)
(['T', 'L', 'P', 'R', 'R', 'I', 'Y', 'T', 'F', 'Q', 'D', 'I', 'H', 'E', 'V', 'Y', 'R'], 'TLPRRIYTFQDIHEVYR', 0.820690278727941, 2.77)
(['H', 'L', 'P', 'R', 'R', 'I', 'Y', 'T', 'F', 'Q', 'D', 'I', 'H', 'E', 'V', 'Y', 'R'], 'HLPRRIYTFQDIHEVYR', 0.84, 2.62)
(['H', 'L', 'M', 'P', 'R', 'I', 'Y', 'R', 'R', 'W', 'R', 'I', 'Y', 'A', 'F', 'W', 'E', 'I', 'Q'], 'HLMPRIYRRWRIYAFWEIQ', 0.866342546345783, 2.58)
(['D', 'V', 'P', 'R', 'R', 'I', 'Y', 'R', 'R', 'S', 'N', 'I', 'Y', 'A', 'F', 'W', 'E', 'I', 'Q'], 'DVPRRIYRRSNIYAFWEIQ', 0.8996919197295268, 2.28)
(['D', 'L', 'P', 'R', 'R', 'I', 'Y', 'T', 'F', 'S', 'R', 'I', 'Y', 'A', 'F', 'Y', 'R'], 'DLPRRIYTFSRIYAFYR', 0.8317418839584276, 2.69)
(['H', 'L', 'M', 'R', 'W', 'G', 'K', 'T', 'F', 'S', 'N', 'I', 'Y', 'H', 'H', 'R', 'I', 'I'], 'HLMRWGKTFSNIYHHRII', 0.9044368527903197, 1.88)
(['T', 'L', 'P', 'V', 'W', 'G', 'K', 'R', 'W', 'N', 'R', 'C'], 'TLPVWGKRWNRC', 0.9456140470742394, 1.29)
(['D', 'L', 'W', 'V', 'W', 'G', 'K', 'L', 'W', 'N', 'R', 'I', 'Y', 'A', 'F', 'W', 'E', 'I', 'Q'], 'DLWVWGKLWNRIYAFWEIQ', 0.9112467355625531, 1.74)
(['T', 'L', 'P', 'R', 'R', 'I', 'Y', 'T', 'F', 'S', 'R', 'I', 'S', 'E', 'V', 'Y', 'E', 'I', 'Q'], 'TLPRRIYTFSRISEVYEIQ', 0.860885641717352, 2.58)
(['N', 'L', 'P', 'R', 'R', 'I', 'Y', 'T', 'F', 'Q', 'D', 'I', 'H', 'E', 'V', 'Y', 'R'], 'NLPRRIYTFQDIHEVYR', 0.8415791011545608, 2.59)
(['D', 'V', 'P', 'R', 'R', 'I', 'Y', 'R', 'R', 'S', 'N', 'I', 'Y', 'H', 'H', 'R', 'I', 'I'], 'DVPRRIYRRSNIYHHRII', 0.9033933544424851, 2.01)
(['H', 'L', 'P', 'R', 'R', 'I', 'Y', 'T', 'W', 'G', 'T', 'C', 'H', 'H', 'H', 'F'], 'HLPRRIYTWGTCHHHF', 0.9138644628745257, 1.67)
(['T', 'V', 'P', 'R', 'P', 'I', 'Y', 'R', 'R', 'W', 'F', 'R', 'K', 'N'], 'TVPRPIYRRWFRKN', 0.9039464588945918, 1.91)
(['T', 'V', 'P', 'R', 'P', 'I', 'Y', 'R', 'R', 'W', 'F', 'R', 'K', 'A', 'F', 'W', 'E', 'I', 'Q'], 'TVPRPIYRRWFRKAFWEIQ', 0.9005430741757448, 2.03)
(['N', 'E', 'P', 'C', 'P', 'F', 'F', 'Q', 'R', 'F', 'Q', 'T', 'V', 'I', 'C', 'C'], 'NEPCPFFQRFQTVICC', 0.9869055718197834, -0.43)
(['D', 'L', 'P', 'C', 'P', 'F', 'P', 'R', 'W', 'N', 'R', 'I', 'Y', 'H', 'Y', 'V', 'M'], 'DLPCPFPRWNRIYHYVM', 0.9241547590678753, 1.61)
(['A', 'H', 'S', 'F', 'R', 'I', 'F', 'D', 'R', 'W', 'F', 'K', 'R', 'H', 'H', 'F'], 'AHSFRIFDRWFKRHHF', 0.9448864661743124, 1.45)
(['A', 'H', 'S', 'F', 'R', 'I', 'F', 'D', 'R', 'W', 'F', 'K', 'R', 'A', 'F', 'C', 'I', 'I'], 'AHSFRIFDRWFKRAFCII', 0.9551952750039726, 0.79)
(['H', 'L', 'M', 'P', 'C', 'P', 'F', 'P', 'R', 'W', 'F', 'R', 'K', 'N'], 'HLMPCPFPRWFRKN', 0.9303912551366692, 1.51)
(['N', 'E', 'P', 'C', 'P', 'F', 'P', 'R', 'W', 'N', 'R', 'I', 'Y', 'H', 'Y', 'V', 'M'], 'NEPCPFPRWNRIYHYVM', 0.9257961559158303, 1.56)
(['R', 'D', 'S', 'Y', 'R', 'I', 'P', 'Q', 'R', 'F', 'K', 'R', 'A', 'F', 'W', 'E', 'E'], 'RDSYRIPQRFKRAFWEE', 0.94598429961045, 1.27)
(['D', 'L', 'P', 'R', 'R', 'I', 'Y', 'T', 'F', 'Q', 'D', 'I', 'H', 'A', 'F', 'Y', 'R'], 'DLPRRIYTFQDIHAFYR', 0.8348101394362377, 2.64)
(['D', 'L', 'P', 'R', 'R', 'I', 'Y', 'T', 'F', 'Q', 'D', 'I', 'H', 'E', 'V', 'Y', 'R'], 'DLPRRIYTFQDIHEVYR', 0.8306742743041697, 2.69)
(['T', 'V', 'P', 'R', 'R', 'I', 'Y', 'T', 'F', 'Q', 'D', 'I', 'H', 'E', 'V', 'Y', 'R'], 'TVPRRIYTFQDIHEVYR', 0.8276507110940771, 2.72)
(['H', 'L', 'M', 'P', 'R', 'I', 'Y', 'R', 'R', 'W', 'F', 'R', 'K', 'N'], 'HLMPRIYRRWFRKN', 0.8939824924937496, 2.42)
(['T', 'L', 'P', 'R', 'R', 'I', 'Y', 'R', 'R', 'W', 'R', 'I', 'Y', 'A', 'F', 'W', 'E', 'I', 'Q'], 'TLPRRIYRRWRIYAFWEIQ', 0.8700187747216046, 2.47)
"""

file_content2 = """
(['D', 'S', 'W', 'F', 'R', 'I', 'Y', 'E', 'Q', 'M', 'R', 'T', 'Q', 'R'], 'DSWFRIYEQMRTQR', 0.8908605401169044, 2.6)
(['D', 'S', 'W', 'F', 'R', 'I', 'E', 'Q', 'M', 'R', 'T', 'Q', 'D', 'R', 'V', 'A', 'W', 'H'], 'DSWFRIEQMRTQDRVAWH', 0.8020881605312414, 2.7)
(['S', 'W', 'W', 'H', 'H', 'H', 'K', 'Y', 'M', 'R', 'Q', 'L', 'A', 'R', 'I', 'S', 'H'], 'SWWHHHKYMRQLARISH', 0.8966918110874875, 2.44)
(['D', 'W', 'W', 'H', 'H', 'H', 'K', 'Y', 'M', 'R', 'Q', 'Q', 'D', 'R', 'V', 'A', 'W', 'H'], 'DWWHHHKYMRQQDRVAWH', 0.9551569187034907, 2.17)
(['N', 'F', 'Q', 'K', 'H', 'I', 'K', 'T', 'F', 'R', 'T', 'Q', 'D', 'R', 'I', 'S', 'E'], 'NFQKHIKTFRTQDRISE', 0.9370662728011929, 2.25)
(['N', 'F', 'Q', 'K', 'R', 'I', 'K', 'T', 'F', 'I', 'Y', 'N', 'E', 'N', 'I', 'S', 'H'], 'NFQKRIKTFIYNENISH', 0.969195927362655, 1.95)
(['N', 'F', 'Q', 'K', 'R', 'I', 'K', 'T', 'F', 'R', 'T', 'Q', 'D', 'R', 'I', 'S', 'H'], 'NFQKRIKTFRTQDRISH', 0.9164703726464001, 2.35)
(['D', 'S', 'W', 'W', 'H', 'H', 'G', 'V', 'Q', 'R', 'T', 'Q', 'D', 'R', 'I', 'S', 'E'], 'DSWWHHGVQRTQDRISE', 0.8952691890748266, 2.48)
(['S', 'W', 'T', 'Q', 'K', 'R', 'I', 'C', 'N', 'F', 'W', 'W', 'N', 'E', 'N', 'V', 'A', 'W', 'H'], 'SWTQKRICNFWWNENVAWH', 0.9725780450613052, 1.56)
(['D', 'S', 'W', 'F', 'R', 'I', 'C', 'N', 'M', 'R', 'A', 'M', 'D', 'R', 'I', 'S', 'P', 'C'], 'DSWFRICNMRAMDRISPC', 0.9696703800332107, 1.71)
(['D', 'S', 'W', 'F', 'R', 'I', 'Y', 'E', 'Q', 'M', 'R', 'N', 'E', 'N', 'I', 'S', 'H'], 'DSWFRIYEQMRNENISH', 0.9053715280250239, 2.42)
(['D', 'S', 'W', 'F', 'R', 'I', 'Y', 'E', 'Q', 'M', 'R', 'Q', 'D', 'R', 'I', 'S', 'E'], 'DSWFRIYEQMRQDRISE', 0.841137093956458, 2.7)
(['N', 'F', 'Q', 'K', 'R', 'I', 'K', 'T', 'F', 'I', 'T', 'N', 'L', 'V', 'K', 'N', 'H'], 'NFQKRIKTFITNLVKNH', 0.981371144579812, 1.43)
"""

file_content3 = """
(['T', 'Y', 'L', 'K', 'W', 'I', 'T', 'R', 'A', 'R', 'C', 'M', 'C', 'K', 'V', 'L', 'C'], 'TYLKWITRARCMCKVLC', 0.9990162490412935, 0.06)
(['D', 'F', 'R', 'W', 'W', 'T', 'E', 'V', 'T', 'Q', 'Q', 'L', 'P', 'E', 'A', 'V', 'R', 'N'], 'DFRWWTEVTQQLPEAVRN', 0.82, 2.25)
(['D', 'F', 'R', 'W', 'W', 'T', 'E', 'V', 'T', 'Q', 'Q', 'L', 'P', 'E', 'A', 'V', 'F', 'Y'], 'DFRWWTEVTQQLPEAVFY', 0.7362293283454607, 2.37)
(['D', 'F', 'R', 'W', 'W', 'T', 'E', 'V', 'T', 'Q', 'H', 'H', 'K', 'E', 'A', 'V', 'F', 'Y'], 'DFRWWTEVTQHHKEAVFY', 0.9041383965547767, 2.21)
(['D', 'F', 'R', 'W', 'W', 'T', 'E', 'V', 'T', 'Q', 'Q', 'P', 'T', 'S', 'V', 'N', 'R', 'V'], 'DFRWWTEVTQQPTSVNRV', 0.8383249859308997, 2.24)
(['T', 'T', 'P', 'R', 'R', 'W', 'Q', 'C', 'T', 'W', 'H', 'H', 'K', 'E', 'A', 'V', 'R'], 'TTPRRWQCTWHHKEAVR', 0.9848887897436147, 1.6)
(['D', 'F', 'R', 'W', 'W', 'W', 'Q', 'L', 'A', 'W', 'H', 'H', 'K', 'E', 'A', 'V', 'F', 'Y'], 'DFRWWWQLAWHHKEAVFY', 0.9367797926222837, 2.19)
(['T', 'Y', 'L', 'K', 'R', 'K', 'P', 'R', 'P', 'W', 'H', 'H', 'K', 'E', 'A', 'V', 'F', 'Y'], 'TYLKRKPRPWHHKEAVFY', 0.9766429451028835, 1.74)
(['D', 'F', 'R', 'W', 'W', 'W', 'Q', 'L', 'A', 'W', 'H', 'H', 'K', 'E', 'A', 'V', 'W', 'W', 'P'], 'DFRWWWQLAWHHKEAVWWP', 0.953885646073012, 2.02)
(['D', 'Y', 'L', 'K', 'R', 'K', 'P', 'R', 'T', 'Q', 'Q', 'P', 'T', 'S', 'V', 'N', 'R', 'V'], 'DYLKRKPRTQQPTSVNRV', 0.9568524331171387, 1.94)
(['T', 'Y', 'L', 'K', 'W', 'W', 'Q', 'L', 'A', 'W', 'H', 'H', 'K', 'E', 'A', 'V', 'F', 'Y'], 'TYLKWWQLAWHHKEAVFY', 0.9677679971727656, 1.93)
(['D', 'F', 'L', 'K', 'R', 'W', 'Q', 'C', 'T', 'K', 'C', 'C'], 'DFLKRWQCTKCC', 0.9999998221074473, -0.34)
(['D', 'F', 'L', 'K', 'R', 'W', 'T', 'R', 'A', 'R', 'C', 'M', 'C', 'K', 'V', 'L', 'C'], 'DFLKRWTRARCMCKVLC', 0.9966387334064778, 0.38)
(['D', 'Y', 'L', 'K', 'R', 'W', 'Q', 'C', 'T', 'K', 'C', 'C'], 'DYLKRWQCTKCC', 1.0, -0.41)
(['T', 'T', 'P', 'R', 'K', 'K', 'P', 'R', 'P', 'W', 'H', 'H', 'P', 'H', 'Y', 'N', 'W', 'W', 'P'], 'TTPRKKPRPWHHPHYNWWP', 0.9896479288239948, 0.8)
(['E', 'T', 'P', 'R', 'K', 'T', 'E', 'R', 'A', 'R', 'C', 'M', 'C', 'K', 'V', 'L', 'C'], 'ETPRKTERARCMCKVLC', 0.9885553249962008, 1.03)
(['D', 'F', 'P', 'R', 'D', 'K', 'P', 'R', 'P', 'I', 'P', 'L', 'P', 'H', 'Y', 'N', 'W', 'W', 'P'], 'DFPRDKPRPIPLPHYNWWP', 0.9864558453608876, 1.22)
(['T', 'Y', 'L', 'K', 'K', 'T', 'P', 'R', 'P', 'W', 'H', 'H', 'K', 'E', 'A', 'V', 'F', 'Y'], 'TYLKKTPRPWHHKEAVFY', 0.9759375756656034, 1.75)
"""

file_content4 = """
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

file_content5 = """
(['W', 'W', 'A', 'R', 'R', 'I', 'Y', 'R', 'M', 'P', 'I', 'T', 'P', 'Q', 'P', 'M', 'R'], 'WWARRIYRMPITPQPMR', 0.7873068177154587, 2.88)
(['H', 'Q', 'P', 'R', 'T', 'I', 'Y', 'R', 'M', 'P', 'I', 'T', 'P', 'Q', 'P', 'M', 'R'], 'HQPRTIYRMPITPQPMR', 0.8819231354740908, 2.57)
(['H', 'Q', 'P', 'V', 'K', 'I', 'Y', 'R', 'M', 'L', 'C'], 'HQPVKIYRMLC', 0.9744274408469927, 1.86)
(['H', 'Q', 'P', 'V', 'K', 'I', 'Y', 'R', 'M', 'Q', 'C'], 'HQPVKIYRMQC', 0.9769640681541694, 1.84)
(['H', 'V', 'W', 'N', 'R', 'I', 'C', 'R', 'M', 'L', 'C'], 'HVWNRICRMLC', 0.9867833698324087, 1.51)
(['H', 'V', 'W', 'N', 'R', 'I', 'Y', 'R', 'M', 'L', 'H', 'K', 'T', 'P', 'R', 'M', 'Y', 'Y', 'T'], 'HVWNRIYRMLHKTPRMYYT', 0.9477539159331412, 2.39)
(['H', 'V', 'A', 'R', 'R', 'I', 'Y', 'R', 'M', 'P', 'I', 'D', 'P', 'Q', 'P', 'A', 'Y'], 'HVARRIYRMPIDPQPAY', 0.8640541783836733, 2.61)
(['H', 'V', 'W', 'N', 'R', 'I', 'Y', 'R', 'M', 'P', 'I', 'T', 'P', 'Q', 'P', 'M', 'R'], 'HVWNRIYRMPITPQPMR', 0.8231928900716603, 2.82)
(['W', 'W', 'A', 'R', 'R', 'I', 'C', 'R', 'M', 'Q', 'C'], 'WWARRICRMQC', 0.9832206556984151, 1.73)
(['H', 'Q', 'W', 'W', 'K', 'S', 'Y', 'L', 'A', 'H', 'K', 'T', 'P', 'F', 'P', 'A', 'Y', 'Q', 'Q'], 'HQWWKSYLAHKTPFPAYQQ', 0.989225221903623, 1.21)
(['H', 'V', 'W', 'N', 'K', 'I', 'Y', 'R', 'M', 'L', 'H', 'K'], 'HVWNKIYRMLHK', 0.9686416117406588, 2.24)
(['H', 'Q', 'P', 'V', 'K', 'I', 'Y', 'R', 'M', 'H', 'K', 'Q', 'A', 'R', 'C', 'M', 'R'], 'HQPVKIYRMHKQARCMR', 0.9749772334922384, 1.84)
(['H', 'G', 'W', 'R', 'R', 'I', 'C', 'R', 'M', 'T', 'C'], 'HGWRRICRMTC', 0.987570140433206, 1.24)
(['H', 'W', 'A', 'R', 'R', 'I', 'Y', 'R', 'M', 'P', 'I', 'T', 'P', 'Q', 'P', 'M', 'R'], 'HWARRIYRMPITPQPMR', 0.8261513097742481, 2.76)
(['H', 'W', 'A', 'R', 'R', 'I', 'Y', 'Y', 'A', 'H', 'K', 'Q', 'A', 'R', 'C', 'M', 'R'], 'HWARRIYYAHKQARCMR', 0.9710402366959126, 1.93)
(['H', 'V', 'W', 'N', 'R', 'I', 'Y', 'R', 'M', 'L', 'H', 'K', 'T', 'P', 'R', 'M', 'Y'], 'HVWNRIYRMLHKTPRMY', 0.9205513972416741, 2.42)
"""


# Poziv funkcije
points6 = extract_points(file_content6)
points7 = extract_points(file_content7)
points8 = extract_points(file_content8)
points9 = extract_points(file_content9)
points10 = extract_points(file_content10)

# Poziv funkcije
points1 = extract_points(file_content1)
points2 = extract_points(file_content2)
points3 = extract_points(file_content3)
points4 = extract_points(file_content4)
points5 = extract_points(file_content5)

# Labels s nazivima i površinama
labels = [
    ("p=1", 2.5856, len(points1)),
    ("p=2", 2.6115, len(points2)),
    ("p=2.5", 2.3010, len(points3)),
    ("p=2.75", 2.78046, len(points4)),
    ("p=3", 2.7788, len(points5))
]

pareto_fronts = [points1, points2, points3, points4, points5]
visualize_convex_hull(pareto_fronts,labels)

