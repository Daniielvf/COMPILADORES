# Clase para calcular descuentos de clientes

class DescuentoCalculador

# Constante

TASA_IMPUESTO = 0.12

# Constructor

def initialize(nombre_cliente, edad, es_miembro)
    @nombre = nombre_cliente
    @edad = edad
    @es_miembro = es_miembro
end

# Metodo para calcular el precio final

def calcular_precio_final(precio_base, cupon_activo)

    limite_edad = 18

    es_mayor = @edad >= limite_edad
    es_vip = @es_miembro && (precio_base > 100.0)
    aplica_descuento = es_vip || cupon_activo

    if aplica_descuento && !(@edad < 12)
        descuento = precio_base * 0.15
    elsif precio_base != 0.0
        descuento = 5.0
    else
        descuento = 0.0
    end

    precio_con_descuento = precio_base - descuento
    monto_impuesto = precio_con_descuento * TASA_IMPUESTO
    total = precio_con_descuento + monto_impuesto

    puts "Cliente: #{@nombre}"

    return total
end

# Metodo para verificar si es mayor de edad

def verificar_edad

    if @edad >= 18
        puts "El cliente es mayor de edad"
    else
        puts "El cliente es menor de edad"
    end

end

# Metodo para verificar membresia

def verificar_membresia

    if @es_miembro == true
        puts "El cliente tiene membresia"
    else
        puts "El cliente no tiene membresia"
    end

end

# Metodo para calcular descuento adicional

def descuento_adicional(precio)

    descuento_extra = 0.0

    if precio > 500.0
        descuento_extra = precio * 0.10
    elsif precio >= 200.0
        descuento_extra = precio * 0.05
    else
        descuento_extra = 0.0
    end

    return descuento_extra
end

end

# Creacion de clientes

cliente1 = DescuentoCalculador.new("Carlos Perez", 25, true)

cliente2 = DescuentoCalculador.new("Maria Lopez", 17, false)

cliente3 = DescuentoCalculador.new("Juan Garcia", 30, true)

# Calcular precios

total_pagar1 = cliente1.calcular_precio_final(150.50, false)

total_pagar2 = cliente2.calcular_precio_final(80.75, true)

total_pagar3 = cliente3.calcular_precio_final(550.25, false)

# Mostrar resultados

puts "Total a pagar cliente 1: $#{total_pagar1}"

puts "Total a pagar cliente 2: $#{total_pagar2}"

puts "Total a pagar cliente 3: $#{total_pagar3}"

# Verificar edades

cliente1.verificar_edad

cliente2.verificar_edad

cliente3.verificar_edad

# Verificar membresias

cliente1.verificar_membresia

cliente2.verificar_membresia

cliente3.verificar_membresia

# Calcular descuentos adicionales

extra1 = cliente1.descuento_adicional(150.50)

extra2 = cliente2.descuento_adicional(250.00)

extra3 = cliente3.descuento_adicional(600.00)

puts "Descuento adicional cliente 1: $#{extra1}"

puts "Descuento adicional cliente 2: $#{extra2}"

puts "Descuento adicional cliente 3: $#{extra3}"