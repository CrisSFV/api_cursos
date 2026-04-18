# Script PowerShell para consultar RDS MySQL desde cmder
# Uso: .\rds_query.ps1 [comando] [args]

param(
    [string]$Command = "help",
    [string]$Arg1 = "",
    [string]$Arg2 = ""
)

$RDSHost = "db-prueba82.cozu8wwe6bt6.us-east-1.rds.amazonaws.com"
$RDSUser = "admin"
$RDSPassword = "Prueba82!"
$RDSDatabase = "app_db"
$RDSPort = 3306

function Show-Help {
    Write-Host @"
╔════════════════════════════════════════════════════════════════════╗
║           CONSULTAS RDS MySQL desde PowerShell                    ║
╚════════════════════════════════════════════════════════════════════╝

COMANDOS:
  .\rds_query.ps1 databases              Ver todas las BDs
  .\rds_query.ps1 tables                 Ver tablas de app_db
  .\rds_query.ps1 tables <database>      Ver tablas de una BD
  .\rds_query.ps1 structure categories   Ver estructura de tabla
  .\rds_query.ps1 count categories       Contar registros
  .\rds_query.ps1 python                 Ver tablas vía Python

EJEMPLOS:
  .\rds_query.ps1 databases
  .\rds_query.ps1 tables app_db
  .\rds_query.ps1 structure categories
"@
}

function Connect-RDS {
    param([string]$Database = $RDSDatabase)
    
    $ConnectionString = "Server=$RDSHost;Uid=$RDSUser;Pwd=$RDSPassword;Database=$Database;Port=$RDSPort"
    
    try {
        Add-Type -AssemblyName System.Data.MySqlClient -ErrorAction SilentlyContinue
        if (-not [System.Data.MySqlClient]) {
            Write-Host "⚠️  MySqlConnector no disponible, usando Python..." -ForegroundColor Yellow
            return $null
        }
        
        $connection = New-Object System.Data.MySqlClient.MySqlConnection($ConnectionString)
        $connection.Open()
        return $connection
    }
    catch {
        return $null
    }
}

function Get-RDSDatabases {
    Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  📊 BASES DE DATOS EN RDS" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan
    
    & python -c @"
import mysql.connector
try:
    c = mysql.connector.connect(
        host='$RDSHost',
        user='$RDSUser',
        password='$RDSPassword'
    )
    cur = c.cursor()
    cur.execute('SHOW DATABASES;')
    for db in cur.fetchall():
        print(f'  ✓ {db[0]}')
    c.close()
except Exception as e:
    print(f'❌ Error: {e}')
"@
    Write-Host ""
}

function Get-RDSTables {
    param([string]$Database = "app_db")
    
    Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  📋 TABLAS EN $Database" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan
    
    & python -c @"
import mysql.connector
try:
    c = mysql.connector.connect(
        host='$RDSHost',
        user='$RDSUser',
        password='$RDSPassword',
        database='$Database'
    )
    cur = c.cursor()
    cur.execute('SHOW TABLES;')
    for table in cur.fetchall():
        print(f'  ✓ {table[0]}')
    c.close()
except Exception as e:
    print(f'❌ Error: {e}')
"@
    Write-Host ""
}

function Get-RDSTableStructure {
    param([string]$TableName)
    
    Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  📐 ESTRUCTURA: $TableName" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan
    
    & python -c @"
import mysql.connector
try:
    c = mysql.connector.connect(
        host='$RDSHost',
        user='$RDSUser',
        password='$RDSPassword',
        database='$RDSDatabase'
    )
    cur = c.cursor()
    cur.execute('DESCRIBE $TableName;')
    print(f'{'Field':20} {'Type':30} {'Null':10}')
    print('-' * 60)
    for col in cur.fetchall():
        field = str(col[0]) if isinstance(col[0], bytes) else col[0]
        col_type = str(col[1]) if isinstance(col[1], bytes) else col[1]
        null = str(col[2]) if isinstance(col[2], bytes) else col[2]
        print(f'{field:20} {col_type:30} {null:10}')
    c.close()
except Exception as e:
    print(f'❌ Error: {e}')
"@
    Write-Host ""
}

function Get-RDSTableCount {
    param([string]$TableName)
    
    & python -c @"
import mysql.connector
try:
    c = mysql.connector.connect(
        host='$RDSHost',
        user='$RDSUser',
        password='$RDSPassword',
        database='$RDSDatabase'
    )
    cur = c.cursor()
    cur.execute('SELECT COUNT(*) FROM $TableName;')
    count = cur.fetchone()[0]
    print(f'\n📊 $TableName: {count} registros\n')
    c.close()
except Exception as e:
    print(f'❌ Error: {e}')
"@
}

# Procesar comando
switch ($Command.ToLower()) {
    "databases" { Get-RDSDatabases }
    "tables" {
        if ($Arg1) {
            Get-RDSTables -Database $Arg1
        } else {
            Get-RDSTables
        }
    }
    "structure" {
        if ($Arg1) {
            Get-RDSTableStructure -TableName $Arg1
        } else {
            Write-Host "❌ Especifica una tabla: .\rds_query.ps1 structure <tabla>" -ForegroundColor Red
        }
    }
    "count" {
        if ($Arg1) {
            Get-RDSTableCount -TableName $Arg1
        } else {
            Write-Host "❌ Especifica una tabla: .\rds_query.ps1 count <tabla>" -ForegroundColor Red
        }
    }
    "python" {
        Write-Host "📊 Ejecutando Python..." -ForegroundColor Cyan
        & python view_rds.py all
    }
    default {
        Show-Help
    }
}
