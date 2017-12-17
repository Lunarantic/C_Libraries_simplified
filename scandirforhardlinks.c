#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <string.h>

void scandirforinodes(const char *path, ino_t inodetofind) {
	DIR *dir = opendir(path);
	if (dir == NULL) {
		perror("Couldn't open dir");
		exit(1);
	}
	struct dirent *ent;
	struct stat st;
	char buf[1024];
	while ((ent = readdir(dir)) != NULL) {
		snprintf(buf, sizeof(buf), "%s/%s", path, ent->d_name);
		if (stat(buf, &st) < 0) {
			perror("stat");
			continue;
		}
		if (inodetofind != -1 && ent->d_ino == inodetofind) {
			printf("%s\n", ent->d_name);
		}
		if (!S_ISREG(st.st_mode)) {
			if (inodetofind != -1 && strcmp(ent->d_name, ".") != 0 && strcmp(ent->d_name, "..") != 0) {
				scandirforinodes(ent->d_name, inodetofind);
			}
			continue;
		}
		if (inodetofind == -1 && st.st_nlink > 1) {
			printf("%s in %s is a hard link with refcount: %d\n", ent->d_name, path, st.st_nlink);
			scandirforinodes(path, ent->d_ino);
		} 
	}
	closedir(dir);
}

int main (int argc, char *argv[])
{
	if (argc != 2) {
		fprintf(stderr, "Usage: ./%s directory\n\n", argv[0]);
		exit(1);
	}
	const char *path = argv[1];
	scandirforinodes(path, -1);
	return 0;
}
