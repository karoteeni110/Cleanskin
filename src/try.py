
def can_i_pop():
    a=a.pop(1, None)
    a=a.pop(99,None)
    return

if __name__ == "__main__":
    a = {str(i):i for i in range(10)}
    print(a)
    can_i_pop()
    print(a)
