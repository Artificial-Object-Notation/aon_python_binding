from aon import json_to_aon, aon_to_json
import json

if __name__ == "__main__":
    data = {
        "id": 1,
        "nome": "Alice",
        "profile": {
            "enderecos": [
                {"cep": "06114020", "rua": "Rua das Dores"},
                {"cep": "06114021", "rua": "Rua Azul"},
            ],
            "idade": 30,
        },
    }

    json_str = json.dumps(data, ensure_ascii=False)
    print("==== JSON → AON ====")
    aon = json_to_aon(json_str, "users")
    print(aon)

    print("\n==== AON → JSON ====")
    back = aon_to_json(aon)
    print(back)
