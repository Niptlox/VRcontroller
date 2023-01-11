def open_file_obj(path, scale=1, _convert_faces_to_lines=False, ):
    if isinstance(scale, int):
        scale = (scale, scale, scale)
    with open(path, "r") as f:
        lines = f.readlines()

    vertexes = []
    faces = []
    vertex_index_offset = 0
    i = 0
    for line in lines:
        i += 1
        if not line.replace(" ", "") or line[0] == "#":
            continue
        try:
            b = line.split()[0]
        except Exception as ex:
            b = None
            print(f"Warning line {i} open obj", line, ex)

        if b == "o":
            # object
            vertex_index_offset = len(vertexes)
        if b == "v":
            split = line.split()
            vertex = [float(split[i + 1]) * scale[i] for i in range(3)]
            vertexes.append(vertex)
        if b == "f":
            face = [int(st.split("/")[0]) - 1 for st in line.split(" ")[1:]]
            faces.append(face)
    if _convert_faces_to_lines:
        return vertexes, convert_faces_to_lines(faces), faces
    return vertexes, faces


def convert_faces_to_lines(faces):
    lines = set()
    for face in faces:
        lines.add(tuple(sorted((face[0], face[-1]))))
        lines |= {tuple(sorted((face[i], face[i + 1]))) for i in range(len(face) - 1)}

    return lines
