// g++ GOL_sdl.cpp -w -lSDL2 -lSDL2_image -o GOL

//Using SDL, SDL_image, standard IO, math, and strings
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <stdio.h>
#include <string>
#include <cmath>
#include <vector>
// header de GOL
#include "GOL_header.h"

//Starts up SDL and creates window
bool init(int SCREEN_WIDTH, int SCREEN_HEIGHT);

//Loads media
bool loadMedia();

//Frees media and shuts down SDL
void close();

//Loads individual image as texture
//SDL_Texture* loadTexture( std::string path );

//The window we'll be rendering to
SDL_Window* gWindow = NULL;

//The window renderer
SDL_Renderer* gRenderer = NULL;

bool init(int SCREEN_WIDTH, int SCREEN_HEIGHT)
{
	//Initialization flag
	bool success = true;

	//Initialize SDL
	if( SDL_Init( SDL_INIT_VIDEO ) < 0 )
	{
		printf( "SDL could not initialize! SDL Error: %s\n", SDL_GetError() );
		success = false;
	}
	else
	{
		//Set texture filtering to linear
		if( !SDL_SetHint( SDL_HINT_RENDER_SCALE_QUALITY, "1" ) )
		{
			printf( "Warning: Linear texture filtering not enabled!" );
		}

		//Create window
		gWindow = SDL_CreateWindow( "GOL", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN );
		if( gWindow == NULL )
		{
			printf( "Window could not be created! SDL Error: %s\n", SDL_GetError() );
			success = false;
		}
		else
		{
			//Create renderer for window
			gRenderer = SDL_CreateRenderer( gWindow, -1, SDL_RENDERER_ACCELERATED );
			if( gRenderer == NULL )
			{
				printf( "Renderer could not be created! SDL Error: %s\n", SDL_GetError() );
				success = false;
			}
			else
			{
				//Initialize renderer color
				SDL_SetRenderDrawColor( gRenderer, 165, 165, 165, 255 );

				//Initialize PNG loading
				int imgFlags = IMG_INIT_PNG;
				if( !( IMG_Init( imgFlags ) & imgFlags ) )
				{
					printf( "SDL_image could not initialize! SDL_image Error: %s\n", IMG_GetError() );
					success = false;
				}
			}
		}
	}

	return success;
}

bool loadMedia()
{
	//Loading success flag
	bool success = true;

	//Nothing to load
	return success;
}

void close()
{
	//Destroy window
	SDL_DestroyRenderer( gRenderer );
	SDL_DestroyWindow( gWindow );
	gWindow = NULL;
	gRenderer = NULL;

	//Quit SDL subsystems
	IMG_Quit();
	SDL_Quit();
}


int main( int argc, char* args[] )
{ // pp_side -> pixels per side
  // n_cell -> identificar el barrido del array, para el render
  const int n_rows = 60, n_cols = 100, pp_side = 8, pp_line = 1;

	int i, j; // contadores para barrido
	int r, c; // row y column

	bool is_init = true;

  // inicializando la lattice y la vecindad
  int **lattice = NULL, **n_lattice = NULL, neighbourhood[3][3] = {};

  // lista de la posición de las células vivas
  //int al_cells[5][2] = {{10,11},{15,14},{24,8},{7,11},{9,1}};
  //Screen dimension constants
  const int SCREEN_WIDTH = n_cols * (pp_side + pp_line)-pp_line;
  const int SCREEN_HEIGHT = n_rows * (pp_side + pp_line)-pp_line;
  const int TOTAL_CELLS = n_rows * n_cols;

  // // INICIALIZACIÓN DE LOS ESTADOS
	std::vector<SDL_Rect> live_cells, death_cells;

	// Generación de la lattice
  lattice = new int *[n_rows];
  n_lattice = new int *[n_rows];
  for (i = 0; i < n_rows; i++){
    lattice[i] = new int[n_cols];
    n_lattice[i] = new int[n_cols];
  }
  for (i = 0; i < n_rows; i++){
    for (j = 0; j < n_cols; j++) {
      lattice[i][j] = 0;
      n_lattice[i][j] = 0;
    }
  }
  // Término de la creación de la lattice


	// inicializando los gráficos
	SDL_Window  * window = nullptr;
  SDL_Renderer * renderer = nullptr;
  SDL_Texture * texture = nullptr;
  SDL_Surface * surface = nullptr;

	//Start up SDL and create window
	if (SDL_Init(SDL_INIT_VIDEO < 0)){
		printf("VIDEO NOT INITIALIZED:\t%s\n", SDL_GetError());
		return -1;
	}

	window = SDL_CreateWindow("GOL",
														SDL_WINDOWPOS_UNDEFINED,
														SDL_WINDOWPOS_UNDEFINED,
														SCREEN_WIDTH,
														SCREEN_HEIGHT,
														SDL_WINDOW_SHOWN);

	if (window == nullptr) {
		printf("WINDOW NOT CREATED:    %s\n", SDL_GetError());
    SDL_Quit();
    return -1;
	}

	renderer = SDL_CreateRenderer( window, -1,
								SDL_RENDERER_ACCELERATED);

	if (renderer == nullptr){
	SDL_DestroyWindow(window);
  printf("RENDERER NOT CREATED:    %s\n", SDL_GetError());
	SDL_Quit();
	return -1;
  }


	SDL_SetRenderDrawColor( renderer, 165, 165, 165, 255 );

	bool quit = false;

	SDL_Event e;

	while(!quit)
	{
		while ( SDL_PollEvent(&e) !=0 )
		{
			if (e.type == SDL_QUIT)
			{
				quit = true;
			}

			if (is_init){

				if (e.type == SDL_KEYDOWN) {
					switch (e.key.keysym.sym) {
						case SDLK_RETURN: // enter presionado
						is_init = false;
					}
				}

				// selección de los cuadros negros
				else if (e.button.button == SDL_BUTTON_LEFT){
					printf("--- LEFT PUSHED---\n");
					r = e.button.y/ (pp_side + pp_line);
					c = e.button.x/ (pp_side + pp_line);
					printf("x ->  %d; y -> %d\n", e.button.x, e.button.y);
					printf("c ->  %d; r -> %d\n",r,c);

					// célula viva
					lattice[r][c] = 1;
				}
			}
		}

		//Clear screen; gray background
		SDL_SetRenderDrawColor( renderer, 165, 165, 165, 255 );
		SDL_RenderClear( renderer );

		//Render white filled quad
		SDL_SetRenderDrawColor( renderer, 255, 255, 255, 255 );

		// creación de las posiciones de los cuadros
		for (r = 0; r < n_rows; r++){
			for (c = 0; c < n_cols ; c++){
				// para células vivas
				if (lattice[r][c] == 1){
					live_cells.push_back({c*(pp_side +pp_line),r * (pp_side +pp_line), pp_side, pp_side});
				}
				// para células muertas
				else {
					death_cells.push_back({c*(pp_side +pp_line),r * (pp_side +pp_line), pp_side, pp_side});
				}
			}
		}
		// renderización
		for (auto const &w : death_cells) {
			SDL_RenderFillRect( renderer, &w);
		}

		//Render black filled quad
		SDL_SetRenderDrawColor( renderer,0, 0, 0, 255 );
		for (auto const &w : live_cells) {
			SDL_RenderFillRect( renderer, &w);
		}

		//Update screen
		SDL_RenderPresent( renderer );
		// delay de 100 milisegundos
		SDL_Delay(100);
		// free memory de los vectores con las células vivas y muertas
		death_cells.clear();
		live_cells.clear();

		// mientras corresponda a la parte de GOL
		if (!is_init){
			printf("****---------   EVOLUCION  ------------*****\n" );
			evolution(lattice, neighbourhood, n_rows, n_cols, n_lattice);
		}
	}
	//Free resources and close SDL
	close();

	return 0;

}
