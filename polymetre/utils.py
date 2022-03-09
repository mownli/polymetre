def find_lcm(numbers):
	assert numbers
	max_number = max(numbers)
	ret = 0
	residue = 0
	while True:
		ret += max_number
		for i in numbers:
			if residue := ret % i:
				break
		if residue == 0:
			return ret
