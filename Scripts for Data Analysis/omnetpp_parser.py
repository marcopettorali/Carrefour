def parse_scalar_file(filename):
    # let's open the .sca file
    scalar_file = open(filename, "r")

    for line in scalar_file:

        # let's read the line in which the scalar value is present
        if line.startswith("scalar"):
            words = line.split(" ")
            return float(words[3])


def parse_vector_file(filename):
    # let's open the .vec file
    try:
        vector_file = open(filename, "r")
    except:
        filename = filename.replace(".vec", " 2.vec")
        vector_file = open(filename, "r")

    # we begin to read values only after having discovered the code associated to each vector
    stage = 0

    # these are the lists in which collected samples will be put
    response_time_list = []
    wait_time_list = []

    # the two lists are returned as a list of lists
    ret = ["", ""]

    # more information later
    swap = False

    for line in vector_file:

        # let's read the code associated to each statistic's vector in OmNET++
        if line.startswith("vector"):
            words = line.split(" ")

            # let's read the code associated to 'stats_responseTime' vector
            if words[3] == "stats_responseTime:vector":

                # response_time_list will be in the wrong final place in object 'ret'
                # a swap with wait_time_list is needed.
                if int(words[1]) == 1:
                    swap = True
                ret[int(words[1])] = response_time_list

            # let's read the code associated to 'stats_responseTime' vector
            elif words[3] == "stats_waitTime:vector":
                ret[int(words[1])] = wait_time_list

            # let's advance the stage counter
            stage = stage + 1

        # when the two read of the vector lines are completed and the end of the file is reached, exit
        elif (stage == 2) and (line == "\n"):
            break

        # when the two read of the vector lines are completed and a value line is read
        elif (stage == 2) and (not(line.startswith("attr"))):
            words = line.split("\t")

            # add a new value to the correct list
            ret[int(words[0])].append(float(words[3]))

    # let's close the vector_file
    vector_file.close()

    # output must be [response_time_list, wait_time_list]
    # swap the lists if needed
    if swap:
        return [ret[1], ret[0]]
    else:
        return ret
