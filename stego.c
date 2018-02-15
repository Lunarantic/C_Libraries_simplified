#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int find_data_size(FILE *input_file) {
	fseek(input_file, 0, SEEK_END);
	int size = ftell(input_file);
	rewind(input_file);

	return size;
}

int main(int argc, char** argv) {

	if(argc != 5) {
		printf("Usage: %s [-l][-m] <input_image> [<output_image> <message_file>]\n", argv[0]);
		return 0;
        }

	int mode;
	if (!strcmp(argv[1], "-m")) {
		mode = 0;
	} else if (!strcmp(argv[1], "-l")) {
		mode = 1;
	} else {
		printf("Usage: %s [-l][-m] <input_image> [<output_image> <message_file>]\n", argv[0]);
		return 0;
	}

	FILE *input_file, *output_file, *message_file;

	input_file = fopen(argv[2], "rb");
	if (input_file == NULL) {
		printf("Cannot open input file : %s\n", argv[2]);
		return 0;
	}

	message_file = fopen(argv[4], "rb");
	if (message_file == NULL) {
		printf("Cannot open message file : %s\n", argv[4]);
		fclose(input_file);
				return 0;
	}

	output_file = fopen(argv[3], "wb");
	if (output_file == NULL) {
		printf("Cannot open output file : %s\n", argv[3]);
					fclose(input_file);
		fclose(message_file);
					return 0;
	}

	int image_offset = find_data_size(input_file);
	int message_size = find_data_size(message_file) * 8;

	for (int i = 0; i < image_offset - (message_size + 8); i++)
		fputc(fgetc(input_file), output_file);

	for (int i = 0; i < message_size; i += 8) {
		int message_byte = fgetc(message_file);
		for (int j = 0; j < 8; j++)
		{
			int inp_byte = fgetc(input_file);
			if (mode) {
				inp_byte &= ~(1UL << 0);
				int b = (int) ((message_byte >> j) & 1);
				inp_byte &= b;
				fputc(inp_byte, output_file);
			} else {
				inp_byte &= ~(1UL << 7);
				int b = (int) ((message_byte >> j) & 1);
				inp_byte &= b;
				fputc(inp_byte, output_file);
			}
		}
	}

	for (int j = 0; j < 8; j++)
	{
		int inp_byte = fgetc(input_file);
		if (mode) {
			inp_byte &= ~(1UL << 0);
			int b = message_size & ~(1UL << j);
			inp_byte |= b;
			fputc(inp_byte, output_file);
		} else {
			inp_byte &= ~(1UL << 7);
			int b = message_size & ~(1UL << j);
			inp_byte |= b;
			fputc(inp_byte, output_file);
		}
	}

	fclose(input_file);
    fclose(message_file);
	fclose(input_file);

	return 0;
}

