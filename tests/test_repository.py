from sqlalchemy import text

from cosmicpython import model, repository


def test_repository_can_save_a_batch(session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.execute(
        text(
            r"""
            SELECT
                reference,
                sku,
                _purchased_quantity,
                eta
            FROM "batches"
        """
        )
    )

    assert list(rows) == [
        ("batch1", "RUSTY-SOAPDISH", 100, None),
    ]


def insert_order_line(session):
    session.execute(
        text(
            r"""
        INSERT INTO order_lines (order_id, sku, qty)
        VALUES ("order1", "GENERIC-SOFA", 12)  
        """
        )
    )

    [[orderline_id]] = session.execute(
        text(
            rf"""
        SELECT 
            id 
        FROM order_lines 
        WHERE 1=1
            AND order_id="order1"
            AND sku="GENERIC-SOFA"
        """
        )
    )
    return orderline_id


def insert_batch(session, batch_id):
    session.execute(
        text(
            rf"""
        INSERT INTO batch (ref, sku, eta, _purchased_qty, _allocated_lines)
        VALUES ("{batch_id}", "GENERIC-SOFA", 100, 0)   
        """
        )
    )

    [[batch_id]] = session.execute(
        text(
            rf"""
        SELECT 
            ref 
        FROM batches 
        WHERE 1=1
            AND ref={batch_id} 
        """
        )
    )
    return batch_id


def insert_allocation(session, orderline_id, batch_id):
    [[batch_id]] = session.execute(
        text(
            rf"""
        SELECT 
            ref 
        FROM batches 
        WHERE 1=1
            AND ref={batch_id} 
        """
        )
    )
    [[orderline_id]] = session.execute(
        text(
            rf"""
        SELECT 
            id
        FROM order_lines 
        WHERE 1=1
            AND order_id={orderline_id} 
            AND sku="GENERIC-SOFA"
        """
        )
    )
    session.execute(
        text(
            rf"""
        INSERT INTO allocations (ref, sku, eta, _purchased_qty, _allocated_lines)
        VALUES ("{batch_id}", "GENERIC-SOFA", 100, 0)       
        """
        )
    )

    [[batch_id]] = session.execute(
        text(
            rf"""
        SELECT 
            ref 
        FROM batches 
        WHERE 1=1
            AND ref={batch_id} 
        """
        )
    )
    return orderline_id, batch_id


def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)

    repo = repository.SqlAlchemyRepository(session)
    retreived = repo.get("batch1")

    expected = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)

    assert retreived == expected
    assert retreived.sku == expected.sku
    assert retreived._purchased_qty == expected._purchased_qty
    assert retreived._allocations == {
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }
