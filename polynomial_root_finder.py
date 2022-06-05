from functools import partial

# bisection in [a,b)
def bisect(f,interval):
    a = interval[0]
    b = interval[1]

    epsilon = .001

    # return nothing if the endpoints have the same sign, implying no root exists in the interval
    if f(a)*f(b) > epsilon*epsilon : return None

    # return if an endpoint is a root
    if abs(f(a)) < epsilon: return a
    #if abs(f(b)) < epsilon: return b

    # swap
    if f(a)>f(b): a,b = b,a

    # iteration
    for i in range(0,99):
        c = (a+b)/2

        if(f(c)<0.): a=c
        else: b=c
    
    return (a+b)/2

def polynomial(coeffs,x):
    ex = 1
    y = 0

    for i in range(0,len(coeffs)):
        y += coeffs[i]*ex
        ex *= x

    return y

def differentiate(coeffs):
    # power rule
    for i in range(1,len(coeffs)):
        coeffs[i-1] = i*coeffs[i]

    if coeffs:
        coeffs.pop()

    return coeffs

def find_roots(coeffs,interval):
    roots = []

    # compute all derivatives
    derivatives = [coeffs]
    for i in range(1,len(coeffs)):
        # 0th index gives 0 degree polynomial
        derivatives = [ differentiate(derivatives[0].copy()) ] + derivatives

    # prepare sections
    section = []
    for i in range(0,len(coeffs)):
        section.append( [interval[0],interval[0]] )

    # a double for loop that runs 
    for i in range(0,len(coeffs)):
        # increment the section
        section[i][0] = section[i][1]
        section[i][1] = interval[1]

        for j in range(i+1,len(coeffs)):
            a = section[j-1][0]
            b = section[j-1][1]
        
            # approximate the root
            root = bisect( partial(polynomial,derivatives[j]) , [a,b])
            
            if root == None:
                break
            else:
                # increment the section
                section[j][0] = section[j][1]
                section[j][1] = root

                # check if a root was found for the polynomial in question
                if j == len(coeffs)-1:
                    roots.append(root)
                    #return roots
    return roots


# default coefficients
coeffs = [50,-25,-2,1]

# input
s = input("Please enter polynomial coefficients (default 50 -25 -2 1): ")
if s:
    coeffs = [ int(x) for x in s.split() ]

# output
s = ""
for i in range(0,len(coeffs)):
    if i>0: s += " + "
    s += str(coeffs[i]) + "x^" + str(i)
print("Finding roots for: y =",s)

roots = find_roots(coeffs, [-10,10])

print("Roots found: ", roots)