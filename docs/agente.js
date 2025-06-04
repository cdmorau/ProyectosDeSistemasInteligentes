class Agente {
    // Inicializa la clase Agente
    constructor() {
      // Inicializa las figuras del juego (jugador humano y computadora) y el estado del juego
      this.figuras = ['X', 'O'];
      this.jugador_humano = 'X';
      this.jugador_computadora = 'O';
  

    }
  
    // Método que maneja las percepciones del agente
    
    // Sensor que obtiene la figura del jugador humano
    
  
    // Sensor que obtiene el estado actual de la tabla
    
  
    // Actuador que cambia el estado del juego al final de cada turno
    
    
  
    //Actuadores lógicos
  
    seleccionar_figura(figura) {
      this.jugador_humano = figura;
      this.jugador_computadora = this.figuras[(this.figuras.indexOf(figura) + 1) % 2];
    }
  
    
  
    comprobar_ganador(tabla, jugador) {
      return (
        (tabla[0] == jugador && tabla[1] == jugador && tabla[2] == jugador) ||
        (tabla[3] == jugador && tabla[4] == jugador && tabla[5] == jugador) ||
        (tabla[6] == jugador && tabla[7] == jugador && tabla[8] == jugador) ||
        (tabla[0] == jugador && tabla[3] == jugador && tabla[6] == jugador) ||
        (tabla[1] == jugador && tabla[4] == jugador && tabla[7] == jugador) ||
        (tabla[2] == jugador && tabla[5] == jugador && tabla[8] == jugador) ||
        (tabla[0] == jugador && tabla[4] == jugador && tabla[8] == jugador) ||
        (tabla[2] == jugador && tabla[4] == jugador && tabla[6] == jugador)
      );
    }
    
  
    juego_terminado(tablero) {
  
      if (this.comprobar_ganador(tablero, 'O') || this.comprobar_ganador(tablero, 'X')) {
        return true;
      }
  
      if (!tablero.includes('')) {
        return true;
      }
  
      return false;
    }
  
    minimax(tablero, profundidad, maximaxing) { 
  
      // Caso base: retorna el valor de la hoja
      if (this.juego_terminado(tablero)) {
          if (this.comprobar_ganador(tablero, this.jugador_computadora)) {
              return 10 - profundidad;
          } else if (this.comprobar_ganador(tablero, this.jugador_humano)) {
              return profundidad - 10;
          } else {
              return 0;
          }
      }
      if (maximaxing) {
          let mejorPuntaje = Number.NEGATIVE_INFINITY;
          for (let i = 0; i < tablero.length; i++) {
              if (tablero[i] == "") {
                  tablero[i] = this.jugador_computadora;
                  let puntaje = this.minimax(tablero, profundidad + 1, false);
                  tablero[i] = "";
                  mejorPuntaje = Math.max(mejorPuntaje, puntaje);
              }
          }
          return mejorPuntaje;
      }
      else {
          let mejorPuntaje = Number.POSITIVE_INFINITY;
          for (let i = 0; i < tablero.length; i++) {
              if (tablero[i] == "") {
                  tablero[i] = this.jugador_humano;
                  let puntaje = this.minimax(tablero, profundidad + 1, true);
                  tablero[i] = "";
                  mejorPuntaje = Math.min(mejorPuntaje, puntaje);
              }
          }
          return mejorPuntaje;
      }
  }
  
  mejor_movimiento(tabla) {
      
      
      let mejorPuntaje = Number.NEGATIVE_INFINITY;
      let bestMovimiento;
      for (let i = 0; i < tabla.length; i++) {
  
          if (tabla[i] == "") {
              tabla[i] = this.jugador_computadora;
  
              let puntaje = this.minimax(tabla, 0, false);
              tabla[i] = "";
              if (puntaje > mejorPuntaje) {
                  mejorPuntaje = puntaje;
                  bestMovimiento = i;
              }
          }
      }
      
      
      return bestMovimiento;
    }
  
  
  
  
  }
  
  
  
  
  
  const agente = new Agente();
  