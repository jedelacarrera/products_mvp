class LiderUrl:
	def __init__(self, category, subcategory, url):
		self.category = category
		self.subcategory = subcategory
		self.url = url + '?No=0&isNavRequest=Yes&Nrpp=1000&page=1'

	def __repr__(self):
		return '/'.join(self.url.split('/')[5:7])

	def __str__(self):
		return '/'.join(self.url.split('/')[5:7])

info = [
	['Carnes y Pescados', 'vacuno', 'https://www.lider.cl/supermercado/category/Carnes-y-Pescados/Vacuno/_/N-1gleruj'],
	['Carnes y Pescados', 'pollo', 'https://www.lider.cl/supermercado/category/Carnes-y-Pescados/Pollo/_/N-8fisy4'],
	['Carnes y Pescados', 'cerdo', 'https://www.lider.cl/supermercado/category/Carnes-y-Pescados/Cerdo/_/N-smtdkg'],
	['Carnes y Pescados', 'pavo', 'https://www.lider.cl/supermercado/category/Carnes-y-Pescados/Pavo/_/N-k2c2mu'],
	['Carnes y Pescados', 'cordero', 'https://www.lider.cl/supermercado/category/Carnes-y-Pescados/Cordero/_/N-1iidz0s'],
	['Carnes y Pescados', 'pescado y mariscos', 'https://www.lider.cl/supermercado/category/Carnes-y-Pescados/Pescados-y-Mariscos/_/N-xij3cz'],
	['fruta y verdura', 'fruta', 'https://www.lider.cl/supermercado/category/Frutas-y-Verduras/Frutas/_/N-2l8cxe'],
	['fruta y verdura', 'verdura', 'https://www.lider.cl/supermercado/category/Frutas-y-Verduras/Verduras/_/N-1ps6iab'],
	['fruta y verdura', 'frutos secos', 'https://www.lider.cl/supermercado/category/Frutas-y-Verduras/Frutos-Secos/_/N-1h7jpzp'],
	['fruta y verdura', 'disney', 'https://www.lider.cl/supermercado/category/Frutas-y-Verduras/Disney/_/N-16ohr3b'],
	['frescos y lacteos', 'fiambres y embutidos', 'https://www.lider.cl/supermercado/category/Frescos-L%C3%A1cteos/Fiambres-y-Embutidos/_/N-gqb8d6'],
	['frescos y lacteos', 'quesos', 'https://www.lider.cl/supermercado/category/Frescos-L%C3%A1cteos/Quesos/_/N-3j7e1l'],
	['frescos y lacteos', 'leches', 'https://www.lider.cl/supermercado/category/Frescos-L%C3%A1cteos/Leches/_/N-1syzw6g'],
	['frescos y lacteos', 'crema', 'https://www.lider.cl/supermercado/category/Frescos-L%C3%A1cteos/Cremas/_/N-1ozxmgv'],
	['frescos y lacteos', 'bebidos vegetales', 'https://www.lider.cl/supermercado/category/Frescos-L%C3%A1cteos/Bebidas-Vegetales/_/N-xj3z08'],
	['frescos y lacteos', 'yoghurt', 'https://www.lider.cl/supermercado/category/Frescos-L%C3%A1cteos/Yoghurt/_/N-1ywlmf4'],
	['frescos y lacteos', 'postres refrigerados', 'https://www.lider.cl/supermercado/category/Frescos-L%C3%A1cteos/Postres-Refrigerados/_/N-19rajm2'],
	['frescos y lacteos', 'huevos y mantequillas', 'https://www.lider.cl/supermercado/category/Frescos-L%C3%A1cteos/Huevos-y-Mantequillas/_/N-squyhq'],
	['frescos y lacteos', 'comidas preparadas', 'https://www.lider.cl/supermercado/category/Frescos-L%C3%A1cteos/Comidas-Preparadas/_/N-4an7fd'],
	['congelados', 'verduras y frutas congeladas', 'https://www.lider.cl/supermercado/category/Congelados/Verduras-y-Frutas-Congeladas/_/N-19z05nb'],
	['congelados', 'hamburguesa y churrascos', 'https://www.lider.cl/supermercado/category/Congelados/Hamburguesas-y-Churrascos/_/N-th1w9g'],
	['congelados', 'comidas congeladas', 'https://www.lider.cl/supermercado/category/Congelados/Comidas-Congeladas/_/N-g52l8f'],
	['congelados', 'helados', 'https://www.lider.cl/supermercado/category/Congelados/Helados/_/N-ovueji'],
	['despensa', 'alimentacion libre', 'https://www.lider.cl/supermercado/category/Despensa/Alimentaci%C3%B3n-Libre/_/N-1oou206'],
	['despensa', 'pastas y salsas', 'https://www.lider.cl/supermercado/category/Despensa/Pastas-y-Salsas/_/N-pgxorj'],
	['despensa', 'harinas', 'https://www.lider.cl/supermercado/category/Despensa/Harinas-y-Polvos/_/N-1w5ocqy'],
	['despensa', 'arroz y legumbres', 'https://www.lider.cl/supermercado/category/Despensa/Arroz-y-Legumbres/_/N-13kg7b2'],
	['despensa', 'salsas', 'https://www.lider.cl/supermercado/category/Despensa/Salsas/_/N-1188opy'],
	['despensa', 'aceites y aderezos', 'https://www.lider.cl/supermercado/category/Despensa/Aceites-y-Aderezos/_/N-qskffs'],
	['despensa', 'coctel y snack', 'https://www.lider.cl/supermercado/category/Despensa/C%C3%B3ctel-y-Snack/_/N-1o5ibif'],
	['despensa', 'conservas', 'https://www.lider.cl/supermercado/category/Despensa/Conservas/_/N-98vkeb'],
	['despensa', 'reposteria', 'https://www.lider.cl/supermercado/category/Despensa/Reposter%C3%ADa/_/N-1e3xmac'],
	['despensa', 'alimentos instantaneo', 'https://www.lider.cl/supermercado/category/Despensa/Alimentos-Instant%C3%A1neos/_/N-gm6h78'],
	['mundo bebe y jugueteria', 'alimentos y lactancia', 'https://www.lider.cl/supermercado/category/Mundo-Beb%C3%A9-y-Jugueter%C3%ADa/Alimentaci%C3%B3n-y-Lactancia/_/N-1we5k8g'],
	['mundo bebe y jugueteria', 'perfumeria e higiene', 'https://www.lider.cl/supermercado/category/Mundo-Beb%C3%A9-y-Jugueter%C3%ADa/Perfumer%C3%ADa-e-Higiene/_/N-1yt9ipw'],
	['mundo bebe y jugueteria', 'pañales y muda', 'https://www.lider.cl/supermercado/category/Mundo-Beb%C3%A9-y-Jugueter%C3%ADa/Pa%C3%B1ales-y-Muda/_/N-m0dwac'],
	['mundo bebe y jugueteria', 'ropa de bebe', ''],
	['mundo bebe y jugueteria', 'juguetes y actividades', ''],
	['mundo bebe y jugueteria', 'viajes y seguridad de bebe', ''],
	['mascotas', 'perro', 'https://www.lider.cl/supermercado/category/Mascotas/Perro/_/N-12dc08k'],
	['mascotas', 'gato', 'https://www.lider.cl/supermercado/category/Mascotas/Gato/_/N-14sisva'],
	['mascotas', 'otras mascotas', 'https://www.lider.cl/supermercado/category/Mascotas/Otras-Mascotas/_/N-1gc6ake'],
	['desayunos y panaderia', 'panaderia', 'https://www.lider.cl/supermercado/category/Pan-Frutas-y-Verduras/Panader%C3%ADa/_/N-5fhq6y'],
	['desayunos y panaderia', 'cereales', 'https://www.lider.cl/supermercado/category/Desayunos-y-Panader%C3%ADa/Cereales/_/N-1le2ate'],
	['desayunos y panaderia', 'café, te, hierbas', 'https://www.lider.cl/supermercado/category/Desayunos-y-Panader%C3%ADa/Caf%C3%A9-T%C3%A9-y-Hierbas/_/N-wauza0'],
	['desayunos y panaderia', 'dulces, mermelada y manjar', 'https://www.lider.cl/supermercado/category/Desayunos-y-Panader%C3%ADa/Dulces-Mermeladas-y-Manjar/_/N-1j5bt7c'],
	['desayunos y panaderia', 'galletas y colaciones dulces', 'https://www.lider.cl/supermercado/category/Desayunos-y-Panader%C3%ADa/Galletas-y-Colaciones-Dulces/_/N-pbmgle'],
	['desayunos y panaderia', 'chocolates y candies', 'https://www.lider.cl/supermercado/category/Desayunos-y-Panader%C3%ADa/Chocolates-y-Candy/_/N-1juh1iq'],
	['desayunos y panaderia', 'postres para preparar', 'https://www.lider.cl/supermercado/category/Desayunos-y-Panader%C3%ADa/Postres-para-Preparar/_/N-6vmfx7'],
	['desayunos y panaderia', 'pastelería', 'https://www.lider.cl/supermercado/category/Desayunos-y-Panader%C3%ADa/Pasteler%C3%ADa/_/N-qg627'],
	['bebidas y licores', 'deme tres porfavor', 'https://www.lider.cl/supermercado/category/Bebidas-Licores/Deme-3-por-favor/_/N-g02snv'],
	['bebidas y licores', 'vinos y espumantes', 'https://www.lider.cl/supermercado/category/Bebidas-Licores/Vinos-y-Espumantes/_/N-she0ig'],
	['bebidas y licores', 'cervezas', 'https://www.lider.cl/supermercado/category/Bebidas-Licores/Cervezas/_/N-1mi8n3m'],
	['bebidas y licores', 'destilados', 'https://www.lider.cl/supermercado/category/Bebidas-Licores/Destilados/_/N-7n2dag'],
	['bebidas y licores', 'coctel y licores', 'https://www.lider.cl/supermercado/category/Bebidas-Licores/Coctel-y-Licores/_/N-8rxdu7'],
	['bebidas y licores', 'bebidas', 'https://www.lider.cl/supermercado/category/Bebidas-Licores/Bebidas/_/N-o65v3z'],
	['bebidas y licores', 'jugos ', 'https://www.lider.cl/supermercado/category/Bebidas-Licores/Jugos/_/N-oz9aq9'],
	['bebidas y licores', 'aguas', 'https://www.lider.cl/supermercado/category/Bebidas-Licores/Aguas/_/N-1227rw1'],
	['bebidas y licores', 'hielo', 'https://www.lider.cl/supermercado/category/Bebidas-Licores/Hielo/_/N-1pzg9o4'],
	['limpieza y aseo', 'detergentes', 'https://www.lider.cl/supermercado/category/Limpieza-Aseo/Detergentes/_/N-f3yzpu'],
	['limpieza y aseo', 'baño y cocina', 'https://www.lider.cl/supermercado/category/Limpieza-Aseo/Ba%C3%B1o-y-Cocina/_/N-mfbfi0'],
	['limpieza y aseo', 'pisos y muebles', 'https://www.lider.cl/supermercado/category/Limpieza-Aseo/Pisos-y-Muebles/_/N-fotifz'],
	['limpieza y aseo', 'papeles', 'https://www.lider.cl/supermercado/category/Limpieza-Aseo/Papeles/_/N-ncfsxl'],
	['limpieza y aseo', 'aerosoles y desinfectantes', 'https://www.lider.cl/supermercado/category/Limpieza-Aseo/Aerosoles-y-Desinfectantes/_/N-qr95di'],
	['limpieza y aseo', 'accesorios aseo', 'https://www.lider.cl/supermercado/category/Limpieza-Aseo/Accesorios-Aseo/_/N-g6eqjj'],
	['perfumeria y salud', 'cuidado facial-corporal', 'https://www.lider.cl/supermercado/category/Perfumer%C3%ADa-Salud/Cuidado-Facial-Corporal/_/N-1c23u66'],
	['perfumeria y salud', 'cuidado capilar', 'https://www.lider.cl/supermercado/category/Perfumer%C3%ADa-Salud/Cuidado-Capilar/_/N-u3y2c4'],
	['perfumeria y salud', 'cuidado personal', 'https://www.lider.cl/supermercado/category/Perfumer%C3%ADa-Salud/Cuidado-Personal/_/N-1nln3mi'],
	['perfumeria y salud', 'cuidado bucal', 'https://www.lider.cl/supermercado/category/Perfumer%C3%ADa-Salud/Cuidado-Bucal/_/N-hux3cg'],
	['perfumeria y salud', 'cuidado hombre', 'https://www.lider.cl/supermercado/category/Perfumer%C3%ADa-Salud/Cuidado-Hombre/_/N-1o9q315'],
	['perfumeria y salud', 'cuidado mujer', 'https://www.lider.cl/supermercado/category/Perfumer%C3%ADa-Salud/Cuidado-Mujer/_/N-1atuxia'],
	['perfumeria y salud', 'cuidado adulto mayor', 'https://www.lider.cl/supermercado/category/Perfumer%C3%ADa-Salud/Cuidado-Adulto-Mayor/_/N-kl3eff'],
	['perfumeria y salud', 'belleza', 'https://www.lider.cl/supermercado/category/Perfumer%C3%ADa-Salud/Belleza/_/N-u9xnwa'],
	['perfumeria y salud', 'salud', 'https://www.lider.cl/supermercado/category/Perfumer%C3%ADa-Salud/Salud/_/N-7nnagl'],
]

LIDER_URLS = [
	LiderUrl(elem[0], elem[1], elem[2]) for elem in info if len(elem) == 3 and elem[2] != ''
]
