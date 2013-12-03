/*
  A0 -> Entrda analógica (pedal de expressão)
  5 -> Entrada do botão PRÓXIMO
  6 -> Entrada do botão ANTERIOR
*/
int pedal = A0, proximo = 5, anterior = 6;


void setup() {
  Serial.begin(9600);
  pinMode(pedal, INPUT);
  pinMode(proximo, INPUT);
  pinMode(anterior, INPUT);
}
int dist(int v1,int v2) {
  if (v1 >= v2)
    return v1-v2;
  else
    return v2-v1; 
}
int last_pedal=-1, last_valor=-1;
int range = 2;

void loop() {
  int estado_proximo, estado_anterior, estado_pedal, valor = 0;
  estado_proximo = digitalRead(proximo); 
  estado_anterior = digitalRead(anterior);
  estado_pedal = analogRead(pedal); 
  if (estado_anterior)
    valor = 2;
  else if (estado_proximo)
    valor = 1;
  /*
    Imprime prox,pedal
    Sendo prox uma variável que indica a mudança de filtro:
    0- Mesmo filtro
    1- Próximo Filtro
    2- Filtro Anterior
    Pedal indica o quão pressionado está o pedal de expressão.
    ID - 1 (botao)
    ID - 2 (pedal)
  */
  if (valor != last_valor && valor>0) {
     Serial.println("1," + String(valor));
  }
  if (abs(estado_pedal - last_pedal) > range) { 
    Serial.println("2," + String(estado_pedal));
     last_pedal = estado_pedal;  
  }
  last_valor = valor;

  delay(1); /* Delay de 1 ms para estabilidade */
}
