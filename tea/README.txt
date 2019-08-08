# create a table in tea database
```shell
CREATE TABLE black (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  origin VARCHAR(100),
  PRIMARY KEY ( id )
);
```

#### Insert tea
```shell
insert into black (name) VALUES
  ('Irish Breakfast'),
  ('English Breakfast'),
  ('Lapsang Souchong');
```
