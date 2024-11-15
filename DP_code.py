import numpy as np
def zero(s):
    zero_started = False
    for i in range(len(s)):
        if s[i] == '0':
            zero_started = True
        elif zero_started and s[i] == '1':
            return i
    # If the entire string is zeros after the first streak, return the length
    return len(s)

def merge_patterns(pattern1, pattern2):
    """
    Merge two binary patterns using bitwise AND, ensuring non-overlapping zeros.
    """
    return ''.join('1' if pattern1[k] == '1' and pattern2[k] == '1' else '0'
                   for k in range(len(pattern1)))

def one(s):
    one_started = False
    for i in range(len(s)):
        if s[i] == '1':
            one_started = True
        elif one_started and s[i] == '0':
            return i
    # If the entire string is ones after the first streak, return the length
    return len(s)

def rate(s):
    # Count the number of '1's in the string
    num_ones = s.count('1')
    # Calculate the total length of the string
    total_length = len(s)
    # Calculate and return the rate
    return num_ones / total_length if total_length > 0 else 0

def initialize_M(D):
    # Create a matrix M with the same dimensions as D
    rows = len(D)
    cols = len(D[0]) # Handle case where D is empty
    M = [[0 for _ in range(cols)] for _ in range(rows)]
    return M

def andd(s1, s2):
    # Ensure both strings are of the same length
    if len(s1) != len(s2):
        print(s1)
        print(s2)
        raise ValueError("Strings must be of the same length")

    # Perform bitwise AND and return the result as a string
    return ''.join('1' if s1[i] == '1' and s2[i] == '1' else '0' for i in range(len(s1)))

def g(x, y, z):
    # Generate the binary string based on x, y, z
    return '1' * x + '0' * y + '1' * z

def generate_P(D, s, rmin, end0, end1):
    """
    Generate the matrix P which stores the best control execution patterns up to each position.
    """
    # Initialize matrix P with the same dimensions as D
    # print(D)
    t = len(s[0])
    rows = len(s)
    cols = len(s[0])
    print("size:", rows,cols)
    P = [['0'*t for _ in range(cols+1)] for _ in range(rows+1)]
    M=np.zeros((rows+1,cols+1))
    # print(s)
    print("t=",t)
    # Handle the first sub-pattern (i = 1)
    for j in range(1,cols+1):
        if j < end0[1]:
            # Case for j < end0(1): P[1][j] = 1^t (all 1's)
            P[1][j] = '1' * t  # All execution (1's for length j+1)
            M[1][j]=0
        else:
            # Case for j >= end0(1): P[1][j] = 1^2 0 1^(j-3)
            if(rate(s[0][0:j])>=rmin):
              P[1][j] = '1' * end1[1] + '0' * (end0[1]-end1[1]) + '1' * (t - end0[1])
              M[1][j]=D[end1[1]][end0[1]]
            else:
              P[1][j] = '1' * t
              M[1][j]=0

    # Start filling matrix P for i > 1 (from second sub-pattern onwards)
    for i in range(2, rows+1):  # loop through sub-patterns starting from i=2
        for j in range(1,cols+1):  # loop through pattern positions
            # print("for j")
            # print(j,len(D[i]))
            if j < end0[i]:
                # Case: i > 1 and j < end0(i)
                P[i][j] = P[i-1][j]
                M[i][j]=M[i-1][j]
            else:

                # Check the rate of the j-length prefix
                if rate(s[i-1][0:j]) < rmin:
                    # If rate of the prefix is less than rmin, use the previous best pattern
                    M[i][j]=M[i-1][j]
                    P[i][j] = P[i-1][j]
                else:
                    # print(P[i][end1[i]-1])
                    # if(end1[i]-1>1):
                    s0 = andd(P[i][end1[i]-1], '1' * end1[i] + '0' * (end0[i] - end1[i]) + '1' * (t - end0[i]))
                    # print(s0)
                    # If the rate is >= rmin, we apply the merging rule
                    if rate(s0[0:j]) >= rmin:
                        if(M[i-1][j]>=M[i][end1[i]-1]+D[end1[i]][end0[i]]):
                            P[i][j] = P[i-1][j]
                            M[i][j]=M[i-1][j]
                        else:
                            P[i][j]=s0
                            M[i][j]=M[i][end1[i]-1]+D[end1[i]][end0[i]]
                    else:
                        # Otherwise, keep the previous best pattern
                        if(M[i-1][j]>=D[end1[i]][end0[i]]):
                            M[i][j]=M[i-1][j]
                            P[i][j] = P[i-1][j]
                        else:
                            M[i][j]=D[end1[i]][end0[i]]
                            P[i][j]= '1' * end1[i] + '0' * (end0[i] - end1[i]) + '1' * (t - end0[i])

    return P,M


def f(D,s,rmin):
    end0=[0]
    end1=[0]
    rates = [0]

    for i in range(len(s)):
        end0.append(zero(s[i]))
        end1.append(one(s[i]))
        rates.append(rate(s[i]))

    P,M = generate_P(D,s,rmin,end0,end1)

    return P,M


t=8
def lst(i,j):
  return '1' * i + '0' * (j - i) + '1' * (t - j)

values=[[2,3],[2,4],[2,5],[2,6],[3,4],[3,5],[3,6],[3,7],[4,5],[4,6],[4,7],[4,8],[5,6],[5,7],[5,8],[7,8]]
Y= [lst(i,j) for (i,j) in values]
X=[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0.02,0.08,0.15,3.7,0,0],[0,0,0,0,0.05,0.12,3.68,1.67,0],[0,0,0,0,0,0.06,3.6,1.64,1.77],[0,0,0,0,0,0,3.52,1.56,1.72],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0.08],[0,0,0,0,0,0,0,0,0]]
P,M = f(X,Y,0.5)
print(M)
print(P)

