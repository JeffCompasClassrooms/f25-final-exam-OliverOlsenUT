# use capsys
# captured = capsys.readouterr()
# assert captured.out == "[x] bb gun\n"
import pytest
import shutil
from christmas_list import ChristmasList
import pickle
import pathlib

FILEPATH = "christmas_list.pkl"

def describe_christmas_list():
    @pytest.fixture()
    def setup_empty_db():
        db_name, db_copy_name, empty_db_name = FILEPATH, "__" + FILEPATH, "empty_" + FILEPATH
        shutil.copyfile(db_name, db_copy_name)
        shutil.copyfile(empty_db_name, db_name)
        yield
        shutil.move(db_copy_name, db_name)
    
    @pytest.fixture()
    def setup_db():
        db_name, db_copy_name = FILEPATH, "__" + FILEPATH
        shutil.copyfile(db_name, db_copy_name)
        with open(db_name, "wb") as f:
            pickle.dump([{"name": "Nintendo Switch 2", "purchased": False}], f)
        yield
        shutil.move(db_copy_name, db_name)

    @pytest.fixture()
    def setup_no_db():
        db_name, db_copy_name = FILEPATH, "__" + FILEPATH
        shutil.move(db_name, db_copy_name)
        yield
        shutil.move(db_copy_name, db_name)

    def describe_init_db():
        def it_initializes_nonexistant_db(setup_no_db):
            # if setup was correct, there should NOT be anything there
            assert not pathlib.Path(FILEPATH).exists()

            l = ChristmasList(FILEPATH)
            assert pathlib.Path(FILEPATH).exists()


    def describe_load_items():
        def it_loads_empty_db(setup_empty_db):
            l = ChristmasList(FILEPATH)
            assert l.loadItems() == []
        def it_loads_db(setup_db):
            l = ChristmasList(FILEPATH)
            assert l.loadItems() == [{"name": "Nintendo Switch 2", "purchased": False}]

    def describe_save_items():
        def it_saves_empty_db(setup_empty_db):
            l = ChristmasList(FILEPATH)
            l.saveItems([])
            with open(FILEPATH, "rb") as f:
                assert pickle.load(f) == []
        
        def it_saves_db(setup_empty_db):
            l = ChristmasList(FILEPATH)
            # No, I can't afford it.
            items = [{"name": "A BRAND NEW CARRR", "purchased": False}]
            l.saveItems(items) 
            with open(FILEPATH, "rb") as f:
                assert pickle.load(f) == items
    
    def describe_add_item():
        def it_adds_to_empty_db_correctly(setup_empty_db):
            l = ChristmasList(FILEPATH)
            l.add("New Item")
            with open(FILEPATH, "rb") as f:
                assert pickle.load(f) == [{"name": "New Item", "purchased": False}]
        def it_adds_to_db_correctly(setup_db):
            l = ChristmasList(FILEPATH)
            existing_item = {"name": "Nintendo Switch 2", "purchased": False}
            l.add("New Item")
            with open(FILEPATH, "rb") as f:
                assert pickle.load(f) == [existing_item, {"name": "New Item", "purchased": False}]

    def describe_check_off():
        def it_checks_off_existing_item(setup_db):
            l = ChristmasList(FILEPATH)
            l.check_off("Nintendo Switch 2")
            with open(FILEPATH, "rb") as f:
                assert pickle.load(f) == [{"name": "Nintendo Switch 2", "purchased": True}]
        def it_doesnt_check_off_nonexistant_item(setup_empty_db):
            l = ChristmasList(FILEPATH)
            l.check_off("Very Real Item")
    
    def describe_remove():
        def it_removes_existing_item(setup_db):
            l = ChristmasList(FILEPATH)
            l.remove("Nintendo Switch 2")
            with open(FILEPATH, "rb") as f:
                assert pickle.load(f) == []

        def it_doesnt_remove_existing_item(setup_db):
            l = ChristmasList(FILEPATH)
            l.remove("Nintendo Switch 3")
            with open(FILEPATH, "rb") as f:
                assert pickle.load(f) == [{"name": "Nintendo Switch 2", "purchased": False}]
    


if __name__ == "__main__":
    pytest.main()
