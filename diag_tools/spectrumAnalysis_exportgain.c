#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <complex.h>
#include <fftw3.h>
#include <limits.h>

#define PI                      3.14159265359

// File Parameters
#define RAW_FILE_PREFIX         "RAW_DATA_"
#define META_FILE_PREFIX        "RUN_META_"
#define COL_FILE_NAME           "COL"
#define JOB_FILE_NAME           "JOB"
#define CSV_PREFIX              "RUN_"
#define FILE_COUNT_NAME         "fileCount"
#define EXTRA_DATA_SIZE         13
#define CSV_NUM_PREC            20

// Process Parameters
#define MAX_SLICING_FACTOR      400
#define MIN_SLICING_FACTOR      50

// File Parameters
#define STD_STR_SZ              256

// Receiver-Specific Parameters
const int gain_values[]         = { 0, 9, 14, 27, 37, 77, 87, 125, 144, 157, 166, 197, 207, 229, 254, 280, 297, 328, 338, 364, 372, 386, 402, 421, 434, 439, 445, 480, 496 };
const int max_gain_index        = 29;

// Signal Buffer Arrays
unsigned char *time_buffer      = NULL;

// Aux arrays
char fileBuffer[STD_STR_SZ];
char raw_data_path[STD_STR_SZ];
char aux_path[STD_STR_SZ];
unsigned int *col_f;

// Aux variables
int frame_size              = 0;
int intAux                  = 0;
double dblAux               = 0;
double dblAux1              = 0;
double dblAux2              = 0;
double signal_pwr           = 0;
double noise_pwr            = 0;
int cur_fr                  = 0;
double cur_gain             = 0;
fftw_complex cpxAux         = 0;

// File parameters
int curr_run                = 0;
int freq_em                 = 0;
int pulse_ms                = 0;
int lin_scale               = 0;
int map_d                   = 0;
int alpha_c_thres           = 0;
int num_col                 = 0;
int f_drift                 = 0;
int center_freq             = 0;
int f_samp                  = 0;
int timeout_interrupt       = 0;
int num_fra_p_file          = 0;
int num_files               = 0;
int pul_num_sam             = 0;
int bin_em                  = 0;
int data_frame_size         = 0;
int file_frame_size         = 0;
int file_length             = 0;
int sld_fft_stps            = 0;
int ttl_n_fr                = 0;
int max_jump                = 0;
int min_jump                = 0;
int aux1                    = 0;
int aux2                    = 0;
int aux3                    = 0;

// Global Buffers
int *dem_goal_f             = NULL;
int *fft_bin                = NULL;
double *pre_corr            = NULL;
double *cur_corr            = NULL;
double *max_corr            = NULL;
int *max_corr_index         = NULL;
double *valid_gain_values   = NULL;
double **pulse_snr          = NULL;
int **gps_pos               = NULL;
unsigned char **frame       = NULL;
char *gain                  = NULL;
char *data                  = NULL;
double *in_phase            = NULL;
double *quadrature          = NULL;

// FFT buffers
fftw_complex *fft_in;
fftw_complex *fft_out;
fftw_complex *signal_cpx;
fftw_plan fft_plan;
double *fft_abs;

// File Handling Variables
FILE *fileStream;
fftw_complex aux_cpx;

void init_buffers();

void clean_up_memmory();

double    **zero_mat_f(int m, int n);
int       **zero_mat_i(int m, int n);
unsigned char **zero_mat_c(int m, int n);

void load_files();

int loadParameter(int comma);

void run_fft();

void analysis();

int main(int argc, char *argv[]) {


	fftw_init_threads();

	fftw_plan_with_nthreads(4);

	load_files();

	init_buffers();


	analysis();


	clean_up_memmory();

	fftw_cleanup_threads();

	return 0;
}

void init_buffers() {
	fft_in      = (fftw_complex *)fftw_alloc_complex(pul_num_sam);
	fft_out     = (fftw_complex *)fftw_alloc_complex(pul_num_sam);
	signal_cpx  = (fftw_complex *)fftw_alloc_complex(frame_size);
	fft_plan    = fftw_plan_dft_1d(pul_num_sam, fft_in, fft_out, FFTW_FORWARD,
	                               FFTW_MEASURE);
	fft_abs     = (double *)malloc(pul_num_sam * sizeof(double));
	gain        = (char *)malloc(num_fra_p_file * num_files * sizeof(char));
	data        = (char *)malloc(file_length * sizeof(char));
	pulse_snr   = zero_mat_f(num_col, ttl_n_fr);
	gps_pos     = zero_mat_i(ttl_n_fr, 3);
	frame       = zero_mat_c(num_fra_p_file, data_frame_size);
	in_phase    = (double *)malloc(data_frame_size * sizeof(double) / 2);
	quadrature  = (double *)malloc(data_frame_size * sizeof(double) / 2);
}

void clean_up_memmory() {
	fftw_destroy_plan(fft_plan);
	fftw_free(fft_in);
	fftw_free(fft_out);
	fftw_free(signal_cpx);
	free(fft_abs);
	free(col_f);
	free(dem_goal_f);
	free(fft_bin);
	free(pre_corr);
	free(cur_corr);
	free(max_corr);
	free(max_corr_index);
	free(valid_gain_values);
	free(gain);
	free(pulse_snr);
	free(gps_pos);
	free(frame);
	free(data);
	free(in_phase);
	free(quadrature);
}

double **zero_mat_f(int m, int n) {

	double **mat;

	// Memmory Allocation
	mat = (double **)calloc(m, sizeof(double *));
	for (int i = 0; i < m; i++) {
		mat[i] = (double *)calloc(n, sizeof(double));
	}

	// Initializing values (0)
	for (int i = 0; i < m; i++)
		for (int j = 0; j < n; j++) {
			mat[i][j] = 0;
		}

	return mat;
}

int **zero_mat_i(int m, int n) {

	int **mat;

	// Memmory Allocation
	mat = (int **)calloc(m, sizeof(int *));
	for (int i = 0; i < m; i++) {
		mat[i] = (int *)calloc(n, sizeof(int));
	}

	// Initializing values (0)
	for (int i = 0; i < m; i++)
		for (int j = 0; j < n; j++) {
			mat[i][j] = 0;
		}

	return mat;
}

unsigned char **zero_mat_c(int m, int n) {

	unsigned char **mat;

	// Memmory Allocation
	mat = (unsigned char **)calloc(m, sizeof(unsigned char *));
	for (int i = 0; i < m; i++) {
		mat[i] = (unsigned char *)calloc(n, sizeof(unsigned char));
	}

	// Initializing values (0)
	for (int i = 0; i < m; i++)
		for (int j = 0; j < n; j++) {
			mat[i][j] = 0;
		}

	return mat;
}

void load_files() {

	// -----------------------------------------------------------
	// JOB file Loading
	// -----------------------------------------------------------
	fileStream  = fopen(JOB_FILE_NAME, "r");
	// RAW data path loading
	if (fscanf(fileStream, "%s", raw_data_path) == 0) {
		fprintf(stderr, "ERROR Reading Data Config File!\n");
		exit(1);
	}
	// Jumping to the next line of the file
	if (fgets(aux_path, STD_STR_SZ, fileStream) == NULL);
	// Numeric parameters loading
	curr_run        = loadParameter(1);
	freq_em         = loadParameter(1);
	pulse_ms        = loadParameter(1);
	lin_scale       = loadParameter(1);
	map_d           = loadParameter(1);
	alpha_c_thres   = loadParameter(1);
	num_col         = loadParameter(1);
	f_drift         = loadParameter(1);
	fclose(fileStream);
	// -----------------------------------------------------------
	col_f = (unsigned int *)malloc(num_col * sizeof(unsigned int));
	// -----------------------------------------------------------

	// -----------------------------------------------------------
	// COL file Loading
	// -----------------------------------------------------------
	fileStream  = fopen(COL_FILE_NAME, "r");
	for (int i = 0; i < num_col; i++) {
		col_f[i] = loadParameter(0) + f_drift;
	}
	fclose(fileStream);
	// -----------------------------------------------------------

	// -----------------------------------------------------------
	// RAW META file Loading
	// -----------------------------------------------------------
	// Defining META file path
	sprintf(aux_path, "%s%s%06d", raw_data_path, META_FILE_PREFIX, curr_run);
	// Numeric parameters loading
	fileStream          = fopen(aux_path, "r");
	center_freq         = loadParameter(1);
	f_samp              = loadParameter(1);
	timeout_interrupt   = loadParameter(1);
	intAux              = loadParameter(1);
	intAux              = loadParameter(1);
	num_fra_p_file      = loadParameter(1);
	num_files           = loadParameter(1);
	fclose(fileStream);
	// -----------------------------------------------------------
	dem_goal_f          = (int *)malloc(num_col * sizeof(int));
	fft_bin             = (int *)malloc(num_col * sizeof(int));
	pre_corr            = (double *)malloc(num_col * sizeof(double));
	cur_corr            = (double *)malloc(num_col * sizeof(double));
	max_corr            = (double *)malloc(num_col * sizeof(double));
	max_corr_index      = (int *)malloc(num_col * sizeof(int));
	valid_gain_values   = (double *)malloc(max_gain_index * sizeof(double));
	// -----------------------------------------------------------

	// Derived Parameters Calculation
	pul_num_sam         = ceil(f_samp * pulse_ms / 1000);
	bin_em              = ceil(pul_num_sam * freq_em / f_samp);
	for (int i = 0; i < num_col; i++) {
		dem_goal_f[i]   = col_f[i] - center_freq;
		fft_bin[i]      = (int)ceil(pul_num_sam / 2 + ((double)pul_num_sam) * ((
		                                double)dem_goal_f[i]) / f_samp + 1);
	}
	data_frame_size     = (int)((float)timeout_interrupt * ((float)f_samp / 500));
	file_frame_size     = data_frame_size + EXTRA_DATA_SIZE;
	frame_size          = data_frame_size / 2;
	file_length         = file_frame_size * num_fra_p_file;
	sld_fft_stps        = frame_size - pul_num_sam;
	ttl_n_fr            = num_fra_p_file * num_files;
	max_jump            = (int)ceil(((double)(MAX_SLICING_FACTOR * pul_num_sam)) /
	                                1000);
	min_jump            = (int)ceil(((double)(MIN_SLICING_FACTOR * pul_num_sam)) /
	                                1000);
	for (int i = 0; i < max_gain_index; i++) {
		valid_gain_values[i] = pow(10, ((double)gain_values[i]) / 100.0);
	}

}

int loadParameter(int comma) {

	if (fgets(fileBuffer, STD_STR_SZ, fileStream) == NULL) {
		fprintf(stderr, "ERROR Reading Data Config File!\n");
		exit(1);
	}
	if (comma) {
		intAux = 0;
		while (fileBuffer[intAux] != ':') {
			intAux++;
		}
		if (intAux >= STD_STR_SZ) {
			fprintf(stderr, "ERROR Reading Data Config File!\n");
			exit(1);
		}
		return atoi(fileBuffer + intAux + 1);
	}
	return atoi(fileBuffer);
}

void run_fft() {
	fftw_execute(fft_plan);
	for (int i = 0; i < pul_num_sam / 2; i++) {
		fft_abs[i]                  = cabs(fft_out[i + pul_num_sam / 2]) /
		                              pul_num_sam;
		fft_abs[i + pul_num_sam / 2]    = cabs(fft_out[i]) / pul_num_sam;
	}
}

void analysis() {
	for (int i = 0; i < num_files; i++) {

		// File Progress Display

		// Raw file loading
		sprintf(aux_path, "%s%s%06d_%06d", raw_data_path, RAW_FILE_PREFIX, curr_run,
		        i + 1);
		fileStream = fopen(aux_path, "r");
		if (fread(data, 1, file_length, fileStream) != file_length) {
			fprintf(stderr, "ERROR Reading RAW File!\n");
			exit(1);
		}
		fclose(fileStream);

		// Parsing each frame fron the current raw file
		for (int j = 0; j < num_fra_p_file; j++) {

			// Radio data Parsing
			for (int k = 0; k < data_frame_size; k++) {
				frame[j][k] = (unsigned char)data[k + j * file_frame_size];
			}

			// GPS data Parsing
			intAux = i * num_fra_p_file + j;
			for (int k = 0; k < 4; k++) {
				aux1 = ((int)data[(j + 1) * file_frame_size - EXTRA_DATA_SIZE + 0 + k]) &
				       0xFF;
				aux2 = ((int)data[(j + 1) * file_frame_size - EXTRA_DATA_SIZE + 4 + k]) & 0xFF;
				aux3 = ((int)data[(j + 1) * file_frame_size - EXTRA_DATA_SIZE + 8 + k]) & 0xFF;
				gps_pos[intAux][0] |= aux1 << 8 * k;
				gps_pos[intAux][1] |= aux2 << 8 * k;
				gps_pos[intAux][2] |= aux3 << 8 * k;
			}

			// Gain Parsing
			gain[j + i * num_fra_p_file] = data[(j + 1) * file_frame_size - 1];
			cur_gain = valid_gain_values[(int)gain[j + i * num_fra_p_file]];
			cur_gain = log10(cur_gain);
			printf("%f\n", cur_gain);
		}
	}

	// Closing file
	fclose(fileStream);
	// -----------------------------------------------------------
}
