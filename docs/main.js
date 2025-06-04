class Agente {
    // Inicializa la clase Agente
    constructor() {
      // Inicializa las figuras del juego (jugador humano y computadora) y el estado del juego
      this.figuras = ['X', 'O'];
      this.jugador_humano = 'X';
      this.jugador_computadora = 'O';
  

    }
  
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


class Ambiente {
    // Inicializa la clase Agente
    constructor() {
      // Inicializa las figuras del juego (jugador humano y computadora) y el estado del juego
      this.agente = new Agente();
      this.estado= "inicial"
  
      // Asocia la acción 'jugar' con cada botón de la tabla
      const botonesJugar = document.querySelectorAll('.jugar');
      botonesJugar.forEach((boton, index) => {
        boton.addEventListener('click', () => {
          this.percepcion('jugar', boton.dataset.accion, index);
        });
      });
  
      // Asocia la acción 'change' al botón 'change'
      const botonChange = document.getElementById('change');
      botonChange.addEventListener('click', () => {
        this.percepcion('change');
      });
  
      // Asocia la acción 'reset' al botón 'reset'
      const botonReset = document.getElementById('reset');
      botonReset.addEventListener('click', () => {
        this.percepcion('reset');
      });
    }
  
    // Método que maneja las percepciones del agente
    percepcion(percepcion, accion, index) {
      console.log(`El usuario hizo clic en el botón '${percepcion}'`);
      switch (percepcion) {
        case 'jugar':
          // Si el juego no ha terminado, cambia el estado del juego a 'jugando'
          if (this.estado !== 'terminado' ) {
  
            // Si el índice del botón es 9, la computadora hace el siguiente movimiento
            if (index === 9 && this.estado=="inicial") {
              this.estado = 'jugando';
              this.setCasilla(this.agente.mejor_movimiento(this.getTabla()), this.agente.jugador_computadora);
  
            } else if (this.getTabla()[index]===""){
              this.estado = 'jugando';
  
              // Si no, el jugador humano hace su movimiento y luego la computadora hace el siguiente
              this.setCasilla(index, this.agente.jugador_humano);
              this.fin();
  
              if (this.estado!="terminado") {
                this.setCasilla(this.agente.mejor_movimiento(this.getTabla()), this.agente.jugador_computadora);
                this.fin();
  
              }
              
  
            }
          }
          break;
        case 'change':
          // Si el juego no ha empezado, cambia las figuras del jugador humano y la computadora
          if (this.estado === 'inicial') {
            this.agente.seleccionar_figura(this.agente.jugador_computadora);
            this.setFigures();

          }
          break;
        case 'reset':
          // Resetea el juego
          this.reset();
          break;
        default:
          console.log(`Percepción desconocida: '${percepcion}'`);
          break;
      }
    }
  
    // Sensor que obtiene la figura del jugador humano
    getHumano() {
      const humano = document.querySelector('.left').textContent;
      return humano;
    }
  
    // Sensor que obtiene el estado actual de la tabla
    getTabla() {
      const casillas = document.querySelectorAll('.casilla');
      const tabla = [];
      casillas.forEach(function (casilla) {
        tabla.push(String(casilla.textContent));
      });
      return tabla;
    }
  
    // Actuador que cambia el estado del juego al final de cada turno
    fin() {
        let tablero= this.getTabla();
        if (this.agente.juego_terminado(tablero)) {
            this.estado="terminado";
            if (this.agente.comprobar_ganador(tablero, this.agente.jugador_computadora)) {
                document.querySelector('h1').textContent= " 🤖 ¡Triunfo el mal! 🤖"
                
            } else if (this.agente.comprobar_ganador(tablero,this.agente.jugador_humano)) {
                document.querySelector('h1').textContent= "Victoria !"
            } else {
                document.querySelector('h1').textContent= "👨‍🔬Draw🤖"
            }
        }
        else{
            document.querySelector('h1').textContent= "¡Do it!"
    
        }
    
    }
  
    reset() {
      this.estado="inicial";
      const casillas = document.querySelectorAll('.casilla');
      casillas.forEach(casilla => casilla.textContent = '' );
      casillas.forEach(casilla => casilla.className = 'casilla' );
    }
    
    setFigures(){
      
      let left = document.querySelector('.left');
      let right = document.querySelector('.right');
      
      // Intercambia el contenido de los elementos
      let temp = left.innerHTML;
      left.innerHTML = right.innerHTML;
      right.innerHTML = temp;
      
      // Intercambia las clases de los elementos
      left.classList.toggle('O');
      left.classList.toggle('X');
      right.classList.toggle('O');
      right.classList.toggle('X');
  
    }
    
    
    setCasilla(cord,jugadorActual){
  
        const casillaActual = document.querySelectorAll('.casilla')[cord];
        casillaActual.textContent = jugadorActual; // Establecer el valor del jugador actual
        casillaActual.classList.add(jugadorActual); // Añadir la clase de color correspondiente
    
    }
  
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
 
  
  
  
  }
  
  
  
  
  
  const ambiente = new Ambiente();
  

