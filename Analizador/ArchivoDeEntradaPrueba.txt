class DescuentoCalculador
  # Constante
  TASA_IMPUESTO = 0.12

  def initialize(nombre_cliente, edad, es_miembro)
    @nombre = nombre_cliente # Variable de instancia / Cadena
    @edad = edad             # Entero
    @es_miembro = es_miembro # Booleano
  end

  def calcular_precio_final(precio_base, cupon_activo)
    limite_edad = 18 # Variable local / Entero

    es_mayor = @edad >= limite_edad
    es_vip = @es_miembro && (precio_base > 100.0)
    aplica_descuento = es_vip || cupon_activo

    if aplica_descuento && !(@edad < 12)
      descuento = precio_base * 0.15 # Operadores: =, * / Flotante: 0.15
    elsif precio_base != 0.0         # Operador: !=
      descuento = 5.0
    else
      descuento = 0.0
    end

    precio_con_descuento = precio_base - descuento # Operador: -
    monto_impuesto = precio_con_descuento * TASA_IMPUESTO
    total = precio_con_descuento + monto_impuesto   # Operador: +

    puts "Cliente: #{@nombre}"
    return total # Palabra reservada
  end
end

cliente1 = DescuentoCalculador.new("Carlos Perez", 25, true)
total_pagar = cliente1.calcular_precio_final(150.50, false)
puts "Total a pagar: $#{total_pagar}"