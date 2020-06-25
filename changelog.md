0.2.0 (unreleased yet)
-----------------------
* [BREAKING] UID fields defined as nullable will stop populate their value on 
the new model instance saving. If your code relied on the old behavior, please
make sure that all your UID fields don't have the `null=True` attribute or 
populate their values manually in save or in calling code.
