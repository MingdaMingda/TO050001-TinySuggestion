BEGIN {
	FS = OFS = "\t";
	if (N <= 0) N = 10;

	last_key = "#";
	n = 0;
}
{
	if (NF < 4) next;

	key = $1;
	tid = $2;
	score = $3;

	if (score <= 0) next;

	if (key == last_key) {
		if (length(h) >= N) next;
		if (tid in h) next;

		printf("\t%s", tid);
		h[tid] = 1;
	} else {
		if (last_key != "#") printf("\n");

		last_key = key;
		delete h;

		printf("%s\t%s", key, tid);
		h[tid] = 1;
	}
}
END {
	if (last_key != "#") printf("\n");
}

