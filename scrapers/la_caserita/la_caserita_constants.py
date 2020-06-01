class BaseCaseritaRequest:
    base_url = "https://www.caserita.cl/"

    def __init__(self, name, pages=1):
        self.name = name
        self.pages = pages


class LaCaseritaCategory(BaseCaseritaRequest):
    base_url = f"{BaseCaseritaRequest.base_url}catalog/category/view/s/"

    def __init__(self, id, name, pages=1):
        self.id = id
        super().__init__(name, pages)

    @property
    def urls(self):
        url = f"{self.base_url}{self.name}/id/{self.id}/?product_list_limit=36&p="
        return [url + str(page + 1) for page in range(self.pages)]


class LaCaseritaSearch(BaseCaseritaRequest):
    base_url = f"{BaseCaseritaRequest.base_url}catalogsearch/result"

    @property
    def urls(self):
        return [
            f"{self.base_url}?q={self.name}&product_list_limit=36&p={page + 1}"
            for page in range(self.pages)
        ]


LA_CASERITA_CATEGORIES = [
    LaCaseritaCategory(3, "limpieza", 5),
    LaCaseritaCategory(4, "cuidado-personal", 4),
    LaCaseritaCategory(5, "despensa", 5),
    LaCaseritaCategory(6, "lacteos-y-frambres", 2),
    LaCaseritaCategory(8, "frescos-y-congelados", 3),  # Muy justo con 2
    LaCaseritaCategory(9, "bebidas-y-licores", 3),
    LaCaseritaCategory(10, "confites-y-cocktail", 1),
    LaCaseritaCategory(11, "bazar", 1),
    LaCaseritaSearch("azucar"),
    LaCaseritaSearch("aceite", 2),
    LaCaseritaSearch("arroz"),
    LaCaseritaSearch("harina"),
    LaCaseritaSearch("jurel"),
    LaCaseritaSearch("atun", 2),
    LaCaseritaSearch("arvej"),
    LaCaseritaSearch("durazno", 2),
    LaCaseritaSearch("maruchan"),
    LaCaseritaSearch("spaghetti"),
    LaCaseritaSearch("espirales"),
    LaCaseritaSearch("mayonesa"),
    LaCaseritaSearch("tomate"),
    LaCaseritaSearch("club"),
    LaCaseritaSearch("supremo"),
    LaCaseritaSearch("ketchup"),
    LaCaseritaSearch("aji"),
    LaCaseritaSearch("nescafe"),
    LaCaseritaSearch("zuko"),
    LaCaseritaSearch("mate"),
    # LaCaseritaSearch("condensada"), Repetido en leche
    LaCaseritaSearch("maggi"),
    LaCaseritaSearch("maizena"),
    LaCaseritaSearch("detergente", 2),
    LaCaseritaSearch("clor", 2),
    LaCaseritaSearch("fosforos"),
    LaCaseritaSearch("cerveza"),
    LaCaseritaSearch("nectar"),
    # LaCaseritaSearch("nectar watts"),  No encontrado
    # LaCaseritaSearch("cigarro"),  No encontrado: pallmall azul, belmont azul
    LaCaseritaSearch("papel", 2),
    LaCaseritaSearch("pañal"),
    LaCaseritaSearch("prestobarba"),
    LaCaseritaSearch("ladysoft"),
    LaCaseritaSearch("dental"),
    LaCaseritaSearch("ballerina"),
    LaCaseritaSearch("pila"),
    LaCaseritaSearch("leche", 2),
    LaCaseritaSearch("queso"),
    LaCaseritaSearch("yoghurt", 2),
    LaCaseritaSearch("mante"),  # mantequilla y manteca
    LaCaseritaSearch("margarina"),
    LaCaseritaSearch("watts"),  # jugo y mermelada
    LaCaseritaSearch("manjarate"),
    LaCaseritaSearch("kryzpo"),
    LaCaseritaSearch("milo"),
]

COOKIES = {
    "setea_comuna": "43",
    "setea_entrega": "true",
    "setea_region": "13",
    "setea_tipo_entrega": "1",
    "store": "8000-26-1",
}
