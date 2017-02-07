# Crumby-OpenShift

This is a branch of the [crumby](https://github.com/bmweiner/crumby) repo which
has been configured for [OpenShift Online](https://www.openshift.com/).

## Deployment

Create the application:

    rhc app create -s crumby python-2.7 mysql-5.5 --from-code https://github.com/bmweiner/crumby#openshift

Query the database with `rhc ssh`:

    rhc ssh crumby
    mysql -u$OPENSHIFT_MYSQL_DB_USERNAME -p$OPENSHIFT_MYSQL_DB_PASSWORD -h$OPENSHIFT_MYSQL_DB_HOST
    use crumby;
    select * from visits;

Query the database by forwarding ports:

    rhc port-forward
    mysql -u <username> -p -h <host> -P <port>
