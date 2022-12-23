def queensAttack(n, k, r_q, c_q, obstacles):
  obstacles = [[i[0] - 1, i[1] - 1] for i in obstacles]

  r_q = r_q - 1
  c_q = c_q - 1
  n = n - 1
  queen_movements = []
  for i in range(r_q, n):
    queen_movements.append([i, r_q])
  for i in range(0, r_q):
    queen_movements.append([i, r_q])
  for i in range(c_q, n):
    queen_movements.append([c_q, i])
  for i in range(0, c_q):
    queen_movements.append([c_q, i])

  counter_c = c_q
  coutner_r = r_q
  while counter_c < n and coutner_r < r_q:
    if counter_c == c_q and coutner_r == r_q:
      continue
    for o_c, o_r in obstacles:
      if counter_c == o_c and coutner_r == o_r:
        queen_movements.append([c_q, i])
        break;

    queen_movements.append([c_q, i])

    counter_c = counter_c + 1
    coutner_r = coutner_r + 1

  counter_c = c_q
  coutner_r = r_q
  while counter_c > (-1) and coutner_r > (-1):
    if counter_c == c_q and coutner_r == r_q:
      continue
    for o_c, o_r in obstacles:
      if counter_c == o_c and coutner_r == o_r:
        queen_movements.append([c_q, i])
        break;

    queen_movements.append([c_q, i])

    counter_c = counter_c - 1
    coutner_r = coutner_r - 1

  counter_c = c_q
  coutner_r = r_q
  while counter_c < n and coutner_r > (-1):
    if counter_c == c_q and coutner_r == r_q:
      continue
    for o_c, o_r in obstacles:
      if counter_c == o_c and coutner_r == o_r:
        queen_movements.append([c_q, i])
        break;

    queen_movements.append([c_q, i])

    counter_c = counter_c + 1
    coutner_r = coutner_r - 1

  counter_c = c_q
  coutner_r = r_q
  while counter_c > (-1) and coutner_r < r_q:
    if counter_c == c_q and coutner_r == r_q:
      continue
    for o_c, o_r in obstacles:
      if counter_c == o_c and coutner_r == o_r:
        queen_movements.append([c_q, i])
        break;

    queen_movements.append([c_q, i])

    counter_c = counter_c - 1
    coutner_r = coutner_r + 1

  print(n, k, r_q, c_q, queen_movements)
  return len(queen_movements)
  # Write your code here
