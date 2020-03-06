def findPassword(bottom=100000,top=999999):
	number = 0
	for i in range(bottom,top+1):
		password = str(i)
		if all(password[j] <= password[j+1] for j in range(len(password)-1)):
			if any(password[j] == password[j+1] and
				password.count(password[j]) == 2 for j in range(len(password)-1)):
				number += 1
	return number

print(findPassword(273025,767253))