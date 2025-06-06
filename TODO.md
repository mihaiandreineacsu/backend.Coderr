# TODO.md

## ✅ Allgemeine Projektstruktur
- [x] Projektordner mit dem Namen `core` erstellen
- [ ] Separate Apps mit sinnvollem Suffix/Präfix (z. B. `auth_app`, `kanban_app`)
- [ ] Jede App enthält `api/`-Ordner für views, serializers, etc.
- [ ] Admin-Oberfläche aktivieren und nutzbar machen

## ✅ Endpoints
- [ ] Alle laut Dokumentation spezifizierten Endpunkte erstellen
- [ ] Routen ressourcenorientiert definieren (z. B. `/api/boards/42/`)

## ✅ Models
- [ ] Modelle im PascalCase benennen
- [ ] Felder im snake_case
- [ ] Sinnvolle `__str__()` Methoden und `Meta` Optionen setzen
- [ ] Keine Logik in Models
- [ ] Beziehungen korrekt mit `on_delete` und `related_name` definieren

## ✅ Serializers
- [ ] ModelSerializers verwenden
- [ ] Felder explizit angeben (`fields = [...]`, kein `__all__`)
- [ ] Validierungsmethoden implementieren, falls notwendig

## ✅ Views
- [ ] `ModelViewSet` für Standard-CRUD-Endpunkte
- [ ] `APIView` oder `GenericAPIView` für individuelle Endpunkte
- [ ] `queryset` und `serializer_class` als Properties
- [ ] `get_queryset()` bei dynamischem Verhalten
- [ ] Permissions explizit mit `permission_classes`

## ✅ URLs
- [ ] Jede App hat eigene `urls.py`
- [ ] Zentrales Routing in `core/urls.py`
- [ ] Ressourcengerechte URL-Struktur

## ✅ Permissions & Authentifizierung
- [ ] Jede App hat eigene `permissions.py` (falls nötig)
- [ ] Authentifizierungsmechanismen einbauen (z. B. Token, Session)
- [ ] Kombinierte Permissions nutzen (z. B. `IsAuthenticated & IsOwner`)
- [ ] Keine offenen Endpunkte ohne triftigen Grund

## ✅ Clean Code & Dokumentation
- [ ] Jede Methode/Funktion hat eine Aufgabe und max. 14 Zeilen
- [ ] Kein toter Code oder `print()` Befehle
- [ ] Einhaltung von PEP8
- [ ] Kommentare und ggf. Docstrings ergänzen

## ✅ GitHub Setup
- [ ] Aussagekräftige `README.md` (auf Englisch) erstellen
- [ ] `requirements.txt` hinzufügen
- [ ] Nur Backend-Code im Repo (Frontend separat)
- [ ] Keine Datenbank-Dateien commiten

## ✅ Testing
- [ ] Testabdeckung ≥ 95 % mit Postman-Tests
- [ ] Kritische Logik zu 100 % getestet

## ✅ Best Practices
- [ ] Imports gruppiert: Standard, Third-party, lokal
- [ ] Klare Trennung: Models = Datenstruktur, Serializers = Validierung, Views = Logik
- [ ] Korrekte HTTP-Statuscodes zurückgeben
